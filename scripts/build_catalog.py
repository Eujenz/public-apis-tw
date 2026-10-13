#!/usr/bin/env python3
"""
build_catalog.py - 從 YAML 原始資料編譯產出目錄

產出標的：
1. docs/catalog.md: 依分類結構化整理之 Markdown 目錄，包含完整屬性與表格
2. dist/apis.json: 機器可讀之標準 JSON 陣列，依 id 穩定排序
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "apis"
DOCS_CATALOG_MD = ROOT_DIR / "docs" / "catalog.md"
DIST_DIR = ROOT_DIR / "dist"
DIST_JSON = DIST_DIR / "apis.json"

CATEGORY_ORDER = [
    ("Government", "政府與公共資訊"),
    ("Finance & Business", "商業登記與金融財經"),
    ("Weather & Environment", "天氣與環境水情"),
    ("Transportation", "交通與運輸"),
    ("Maps & Geospatial", "地理資訊與國土測繪"),
    ("Culture & Tourism", "文化與觀光"),
    ("Education & Research", "教育與學術研究"),
    ("Healthcare & Public Health", "醫療與公共衛生"),
    ("Developer Tools", "開發者工具與輔助服務"),
    ("Other", "其他開放服務"),
]

def load_apis():
    yaml_files = sorted(list(DATA_DIR.glob("*.yml")) + list(DATA_DIR.glob("*.yaml")))
    apis = []
    for f in yaml_files:
        with open(f, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)
            apis.append(data)
    # 穩定依 id 排序
    apis.sort(key=lambda x: x["id"])
    return apis

def generate_markdown(apis):
    # 分類聚合
    by_category = defaultdict(list)
    verified_count = 0
    candidate_count = 0

    for api in apis:
        if api.get("review_status") == "verified":
            verified_count += 1
            by_category[api["category"]].append(api)
        elif api.get("review_status") == "candidate":
            candidate_count += 1
            # 候選項目不進入正式主表，獨立附註或於專用區塊標示

    lines = []
    lines.append("# 台灣公共與開放 API 目錄 (Public APIs Taiwan Catalog)")
    lines.append("")
    lines.append("> 本文件由原始資料自動產生，請勿手動直接編輯。如需修正請修改 `data/apis/*.yml` 並執行 `uv run python scripts/build_catalog.py`。")
    lines.append("")
    lines.append("## 摘要統計")
    lines.append("")
    lines.append(f"- **正式收錄 (Verified)**: {verified_count} 項")
    lines.append(f"- **候選項目 (Candidate)**: {candidate_count} 項")
    lines.append(f"- **最後編譯時間**: 自動更新於每次建置")
    lines.append("")
    lines.append("## 分類快速導覽")
    lines.append("")
    for cat_en, cat_zh in CATEGORY_ORDER:
        cat_apis = by_category.get(cat_en, [])
        lines.append(f"- [{cat_zh} ({cat_en})](#{cat_en.lower().replace('& ', '').replace(' ', '-')}) ({len(cat_apis)})")
    lines.append("")
    lines.append("---")
    lines.append("")

    for cat_en, cat_zh in CATEGORY_ORDER:
        cat_apis = by_category.get(cat_en, [])
        anchor = cat_en.lower().replace("& ", "").replace(" ", "-")
        lines.append(f"## {cat_zh} ({cat_en})")
        lines.append("")
        if not cat_apis:
            lines.append("*目前此分類尚無已驗證項目。*")
            lines.append("")
            continue

        # 輸出 Markdown 表格
        lines.append("| API 名稱 | 提供者 | 簡介 | 驗證機制 | 費用層級 | HTTPS | CORS | 授權條款 | 官方文件 | 查核等級 |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- | :--- |")

        for item in cat_apis:
            name_display = f"**{item['name_zh']}**"
            if item.get("name_en"):
                name_display += f"<br>`{item['name_en']}`"
            provider = item["provider"]
            desc = item["description_zh"]
            auth = item.get("auth_type", "unknown")
            tier = item.get("access_tier", "unknown")
            https = item.get("https_support", "unknown")
            cors = item.get("cors_support", "unknown")
            license_name = item.get("license_name", "unknown")
            docs_url = item["docs_url"]
            vlevel = item.get("verification_level", "none")

            row = (
                f"| {name_display} | {provider} | {desc} | `{auth}` | `{tier}` | `{https}` | `{cors}` | "
                f"`{license_name}` | [文件連結]({docs_url}) | `{vlevel}` |"
            )
            lines.append(row)

        lines.append("")

    return "\n".join(lines)

def main():
    apis = load_apis()
    print(f"[*] 載入共 {len(apis)} 筆 API 資料...")

    # 1. 產生 docs/catalog.md
    md_content = generate_markdown(apis)
    DOCS_CATALOG_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(DOCS_CATALOG_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[V] 成功產出 Markdown 目錄: {DOCS_CATALOG_MD}")

    # 2. 產生 dist/apis.json
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIST_JSON, "w", encoding="utf-8") as f:
        json.dump(apis, f, ensure_ascii=False, indent=2)
    print(f"[V] 成功產出 JSON 資料檔: {DIST_JSON}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
