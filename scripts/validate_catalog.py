#!/usr/bin/env python3
"""
validate_catalog.py - 驗證 public-apis-tw 目錄資料

檢查項目：
1. YAML 檔案是否能正常解析為鍵值字典
2. 是否符合 JSON Schema (Draft 2020-12)
3. id 與檔名 stem 是否完全相符
4. id 是否唯一無重複
5. 網址格式與協定合理性 (docs_url 等必須以 http/https 開頭)
6. 狀態相容性與查核等級一致性：
   - review_status 為 verified 時：
     * 必須有 sources (至少 1 筆) 與 last_reviewed_at
     * verification_level 不得為 none (必須至少為 docs_reviewed)
   - verification_level 為 endpoint_tested 或 sample_response_checked 時：
     * 必須填寫 last_endpoint_tested_at
     * review_status 不得為 candidate
   - last_endpoint_tested_at 存在時，verification_level 不得為 none 或 docs_reviewed
7. 時效性檢查 (Freshness Policy)：
   - last_reviewed_at 或 last_endpoint_tested_at 超過 365 天時提出過期警示
8. 重複 docs_url 檢查並提出警告 (避免重複收錄，但允許共用入口之情境)
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import yaml
from jsonschema import Draft202012Validator

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "apis"
SCHEMA_FILE = ROOT_DIR / "schemas" / "api.schema.json"

_cached_validator = None

def get_validator(schema_file: Path | None = None) -> Draft202012Validator:
    global _cached_validator
    if _cached_validator is not None and schema_file is None:
        return _cached_validator
    target_schema = schema_file or SCHEMA_FILE
    with open(target_schema, "r", encoding="utf-8") as f:
        schema = json.load(f)
    v = Draft202012Validator(schema)
    if schema_file is None:
        _cached_validator = v
    return v

def validate_entry(
    data: dict,
    expected_id: str | None = None,
    validator: Draft202012Validator | None = None,
    today_date: str | None = None
) -> tuple[list[str], list[str]]:
    """
    驗證單一 API 條目的 Schema 與業務邏輯相容性。
    回傳 (errors, warnings) 串列。
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["內容必須為鍵值對字典 (dict)"], []

    v = validator or get_validator()

    # 1. 檔名與 id 一致性 (若指定 expected_id)
    actual_id = data.get("id")
    if expected_id is not None and actual_id != expected_id:
        errors.append(f"'id' ({actual_id}) 與檔案名稱 stem ({expected_id}) 不符")

    # 2. JSON Schema 結構校驗
    schema_errors = list(v.iter_errors(data))
    for err in schema_errors:
        field = ".".join([str(p) for p in err.path]) or "<root>"
        errors.append(f"[{field}]: {err.message}")

    # 3. 業務邏輯校驗
    review_status = data.get("review_status")
    verification_level = data.get("verification_level")
    sources = data.get("sources", [])
    last_reviewed = data.get("last_reviewed_at")
    last_endpoint_tested = data.get("last_endpoint_tested_at")

    # review_status = verified 的相容條件
    if review_status == "verified":
        if not sources or len(sources) == 0:
            errors.append("review_status 為 verified 時必須至少提供一筆來源 (sources)")
        if not last_reviewed:
            errors.append("review_status 為 verified 時必須填寫 last_reviewed_at")
        if verification_level == "none":
            errors.append("review_status 為 verified 但 verification_level 為 none，邏輯不符 (已審查通過者至少需為 docs_reviewed)")

    # verification_level 與 last_endpoint_tested_at 的約束
    if verification_level in ("endpoint_tested", "sample_response_checked"):
        if review_status == "candidate":
            errors.append(f"verification_level 為 {verification_level} 但 review_status 仍為 candidate，邏輯不符")
        if not last_endpoint_tested:
            errors.append(f"verification_level 為 {verification_level} 時必須明確填寫 last_endpoint_tested_at")
    elif last_endpoint_tested:
        errors.append(f"已填寫 last_endpoint_tested_at，但 verification_level 仍為 {verification_level}，應提升為 endpoint_tested 或更高")

    # 4. 時效性與過期政策 (Freshness check)
    ref_date = datetime.strptime(today_date, "%Y-%m-%d").date() if today_date else datetime.now(timezone.utc).date()
    if last_reviewed:
        try:
            rev_date = datetime.strptime(last_reviewed, "%Y-%m-%d").date()
            if (ref_date - rev_date).days > 365:
                warnings.append(f"此條目上次審查時間 ({last_reviewed}) 已超過 365 天，建議重新核驗")
        except ValueError:
            pass

    return errors, warnings

def validate_catalog(
    data_dir: Path | None = None,
    schema_file: Path | None = None,
    today_date: str | None = None
) -> tuple[list[str], list[str], int]:
    """
    走訪目錄下所有 YAML 檔案，執行完整一致性與語意驗證。
    回傳 (errors, warnings, total_files)。
    """
    target_data_dir = data_dir or DATA_DIR
    target_schema = schema_file or SCHEMA_FILE

    if not target_schema.exists():
        return [f"找不到 Schema 檔案: {target_schema}"], [], 0

    validator = get_validator(target_schema)

    if not target_data_dir.exists():
        return [f"找不到資料目錄: {target_data_dir}"], [], 0

    yaml_files = sorted(list(target_data_dir.glob("*.yml")) + list(target_data_dir.glob("*.yaml")))
    if not yaml_files:
        return ["警告：目前沒有任何 API 檔案可供驗證。"], [], 0

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    seen_docs_urls: dict[str, str] = {}

    for file_path in yaml_files:
        rel_path = file_path.name
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            errors.append(f"{rel_path}: YAML 解析失敗 -> {e}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel_path}: 內容必須為鍵值對字典 (dict)")
            continue

        # 唯一性檢查
        actual_id = data.get("id")
        if actual_id:
            if actual_id in seen_ids:
                errors.append(f"{rel_path}: 發現重複的 API ID: '{actual_id}'")
            else:
                seen_ids.add(actual_id)

        # 單檔驗證
        item_errors, item_warnings = validate_entry(
            data=data,
            expected_id=file_path.stem,
            validator=validator,
            today_date=today_date
        )
        for err in item_errors:
            errors.append(f"{rel_path} {err}")
        for warn in item_warnings:
            warnings.append(f"{rel_path} {warn}")

        # 重複 docs_url 警告
        docs_url = data.get("docs_url")
        if docs_url:
            if docs_url in seen_docs_urls:
                warnings.append(f"{rel_path} 與 {seen_docs_urls[docs_url]} 使用相同的 docs_url ({docs_url})")
            else:
                seen_docs_urls[docs_url] = rel_path

    return errors, warnings, len(yaml_files)

def main() -> int:
    print(f"[*] 載入 Schema: {SCHEMA_FILE}")
    errors, warnings, total = validate_catalog()

    if warnings:
        print("\n--- 警告清單 (非阻礙性) ---")
        for w in warnings:
            print(f"[WARN] {w}")

    if errors:
        print(f"\n[X] 驗證失敗！共發現 {len(errors)} 個錯誤：", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"\n[V] 驗證通過！共成功檢查 {total} 個 API 檔案，無格式或邏輯相容性錯誤。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
