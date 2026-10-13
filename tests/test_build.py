import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_build_catalog_runner():
    script = ROOT / "scripts" / "build_catalog.py"
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert res.returncode == 0, f"build_catalog.py failed with stderr: {res.stderr}"

    catalog_md = ROOT / "docs" / "catalog.md"
    assert catalog_md.exists(), "docs/catalog.md must be generated"

    dist_json = ROOT / "dist" / "apis.json"
    assert dist_json.exists(), "dist/apis.json must be generated"
    with open(dist_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) >= 10

def test_catalog_markdown_filters_verified_in_main_table():
    catalog_md = ROOT / "docs" / "catalog.md"
    assert catalog_md.exists()
    content = catalog_md.read_text(encoding="utf-8")

    # 主表章節應在附錄之前
    if "## 附錄：待覆核與候選中項目 (Pending & Candidates)" in content:
        main_part, appendix_part = content.split("## 附錄：待覆核與候選中項目 (Pending & Candidates)")
    else:
        main_part = content
        appendix_part = ""

    # 主表章節不得出現 candidate 或 needs_review 的 API ID 或特定標記
    # 例如 candidate 的 tw-air-quality-history 與 dgpa-work-class-cancel
    assert "台灣空氣品質歷史資料檢索 API (候選)" not in main_part
    assert "人事行政總處天然災害停止上班及上課資訊 (歷次統計)" not in main_part
    assert "疾病管制署傳染病統計資料 API" not in main_part
    assert "健保署特約醫療院所名冊資料集 (含介接)" not in main_part

    # 但附錄中應有其記錄
    if appendix_part:
        assert "tw-air-quality-history" in appendix_part or "台灣空氣品質歷史資料檢索 API (候選)" in appendix_part
        assert "needs_review" in appendix_part or "candidate" in appendix_part

def test_build_json_matches_source_yamls_exactly():
    """編譯產出的 dist/apis.json 筆數、識別碼及狀態必須與 data/apis/*.yml 完全一致"""
    import yaml
    data_dir = ROOT / "data" / "apis"
    dist_json_path = ROOT / "dist" / "apis.json"
    assert dist_json_path.exists()

    yaml_files = sorted(list(data_dir.glob("*.yml")) + list(data_dir.glob("*.yaml")))
    with open(dist_json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 1. 筆數必須完全一致
    assert len(json_data) == len(yaml_files), f"JSON 筆數 ({len(json_data)}) 與 YAML 筆數 ({len(yaml_files)}) 不符"

    yaml_entries = {}
    for yf in yaml_files:
        with open(yf, "r", encoding="utf-8") as fp:
            y = yaml.safe_load(fp)
            yaml_entries[y["id"]] = y

    json_entries = {item["id"]: item for item in json_data}

    # 2. 識別碼集合必須完全相等
    assert set(yaml_entries.keys()) == set(json_entries.keys()), "JSON 與 YAML 的 ID 集合不一致"

    # 3. 每筆的 review_status、verification_level、category、provider 必須完全吻合
    for api_id, y_data in yaml_entries.items():
        j_data = json_entries[api_id]
        assert j_data["review_status"] == y_data["review_status"], f"{api_id} review_status 不一致"
        assert j_data["verification_level"] == y_data["verification_level"], f"{api_id} verification_level 不一致"
        assert j_data["category"] == y_data["category"], f"{api_id} category 不一致"
        assert j_data["provider"] == y_data["provider"], f"{api_id} provider 不一致"

