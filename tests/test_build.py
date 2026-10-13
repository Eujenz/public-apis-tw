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
