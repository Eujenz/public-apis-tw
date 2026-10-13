import copy
import json
import subprocess
import sys
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_catalog import validate_entry, validate_catalog

# 基本合規的 sample 條目（用於變異測試）
VALID_ENTRY_SAMPLE = {
    "id": "sample-test-api",
    "name_zh": "測試用範例 API",
    "description_zh": "本項目用於單元測試驗證驗證器之商業邏輯與欄位約束。",
    "category": "Developer Tools",
    "provider": "測試機構",
    "provider_type": "official",
    "docs_url": "https://example.com/docs",
    "api_style": "REST",
    "auth_type": "none",
    "access_tier": "free",
    "https_support": "yes",
    "cors_support": "yes",
    "license_name": "OGDL-Taiwan-1.0",
    "commercial_use": "allowed",
    "service_status": "active",
    "review_status": "candidate",
    "verification_level": "none",
    "last_reviewed_at": "2026-10-14",
    "sources": ["https://example.com/source"]
}

def test_validate_entry_success_on_valid_sample():
    """正常合規樣本必須驗證通過且無錯誤"""
    errors, warnings = validate_entry(VALID_ENTRY_SAMPLE, expected_id="sample-test-api")
    assert errors == [], f"預期無錯誤，但得到: {errors}"

def test_reject_id_mismatch_with_filename():
    """id 與檔名 stem 不相符時必須回報錯誤"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    errors, _ = validate_entry(entry, expected_id="different-filename")
    assert any("與檔案名稱 stem" in e for e in errors)

def test_reject_missing_required_fields():
    """缺少必要欄位（如 provider、docs_url）必須驗證失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    del entry["provider"]
    del entry["docs_url"]
    errors, _ = validate_entry(entry)
    assert len(errors) >= 2
    assert any("'provider' is a required property" in e for e in errors)
    assert any("'docs_url' is a required property" in e for e in errors)

def test_reject_invalid_enum_values():
    """提供無效的 review_status 或 verification_level 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["review_status"] = "super_verified"
    entry["verification_level"] = "deep_hack"
    errors, _ = validate_entry(entry)
    assert any("review_status" in e for e in errors)
    assert any("verification_level" in e for e in errors)

def test_reject_verified_with_none_verification_level():
    """review_status 為 verified 但 verification_level 為 none 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["review_status"] = "verified"
    entry["verification_level"] = "none"
    errors, _ = validate_entry(entry)
    assert any("verification_level 為 none，邏輯不符" in e for e in errors)

def test_reject_verified_missing_sources_or_reviewed_date():
    """review_status 為 verified 但無 sources 或無 last_reviewed_at 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["review_status"] = "verified"
    entry["verification_level"] = "docs_reviewed"
    entry["sources"] = []
    del entry["last_reviewed_at"]
    errors, _ = validate_entry(entry)
    assert any("必須至少提供一筆來源" in e for e in errors)
    assert any("必須填寫 last_reviewed_at" in e for e in errors)

def test_reject_endpoint_tested_missing_tested_date():
    """verification_level 為 endpoint_tested 但未填寫 last_endpoint_tested_at 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["review_status"] = "verified"
    entry["verification_level"] = "endpoint_tested"
    # 未填寫 last_endpoint_tested_at
    errors, _ = validate_entry(entry)
    assert any("必須明確填寫 last_endpoint_tested_at" in e for e in errors)

def test_reject_candidate_with_endpoint_tested():
    """review_status 為 candidate 但 verification_level 為 endpoint_tested 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["review_status"] = "candidate"
    entry["verification_level"] = "endpoint_tested"
    entry["last_endpoint_tested_at"] = "2026-10-14"
    errors, _ = validate_entry(entry)
    assert any("review_status 仍為 candidate，邏輯不符" in e for e in errors)

def test_reject_tested_date_provided_with_none_level():
    """有 last_endpoint_tested_at 但 verification_level 仍為 none 或 docs_reviewed 必須失敗"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["last_endpoint_tested_at"] = "2026-10-14"
    entry["verification_level"] = "none"
    errors, _ = validate_entry(entry)
    assert any("應提升為 endpoint_tested 或更高" in e for e in errors)

def test_warn_on_stale_review_date():
    """上次審核日期超過 365 天時必須提出過期警告 (Freshness Warning)"""
    entry = copy.deepcopy(VALID_ENTRY_SAMPLE)
    entry["last_reviewed_at"] = "2024-01-01"
    errors, warnings = validate_entry(entry, today_date="2026-10-14")
    assert errors == []
    assert any("超過 365 天" in w for w in warnings)

def test_validate_catalog_detects_duplicate_id_in_directory(tmp_path):
    """目錄中若有兩個檔案具有相同 id，validate_catalog 必須攔截重複 id 錯誤"""
    # 建立兩個檔案，具有相同 id
    file1 = tmp_path / "api-one.yml"
    file2 = tmp_path / "api-two.yml"
    
    e1 = copy.deepcopy(VALID_ENTRY_SAMPLE)
    e1["id"] = "duplicate-id"
    e2 = copy.deepcopy(VALID_ENTRY_SAMPLE)
    e2["id"] = "duplicate-id"

    with open(file1, "w", encoding="utf-8") as f:
        yaml.safe_dump(e1, f)
    with open(file2, "w", encoding="utf-8") as f:
        yaml.safe_dump(e2, f)

    errors, _, count = validate_catalog(data_dir=tmp_path)
    assert count == 2
    assert any("發現重複的 API ID: 'duplicate-id'" in e for e in errors)

def test_validate_catalog_cli_exit_code_on_errors(tmp_path):
    """CLI 執行 validate_catalog.py 在有錯誤資料時必須 exit code 1 並印出錯誤"""
    bad_file = tmp_path / "bad.yml"
    bad_data = {"id": "bad", "name_zh": "incomplete"}
    with open(bad_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(bad_data, f)

    # 執行 CLI 指令並指向壞目錄
    script = ROOT / "scripts" / "validate_catalog.py"
    # 用 python -c 執行 validate_catalog 並傳入自訂目錄
    code = f"""
import sys
from pathlib import Path
sys.path.insert(0, r"{ROOT / 'scripts'}")
from validate_catalog import validate_catalog
errors, warnings, count = validate_catalog(data_dir=Path(r"{tmp_path}"))
if errors:
    print(f"FAILED WITH {{len(errors)}} ERRORS")
    sys.exit(1)
sys.exit(0)
"""
    res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert res.returncode == 1
    assert "FAILED WITH" in res.stdout
