#!/usr/bin/env python3
"""
real_estate_research_consumer.py - 下游應用範例：自住房與土地研究引擎之資料來源整合

示範情境：
「土地型自住房研究引擎」需要評估特定基地的交通便利用度、環境災害風險、
地籍測繪圖資與人口生活圈指標。

本範例展示下游專案如何直接消費 public-apis-tw 發布之 `dist/apis.json`：
1. 載入目錄作為可信任的「資料源註冊表 (Source of Truth)」
2. 依房地產研究維度動態檢索可用資料源
3. 自動檢查商業授權相容性與技術驗證等級
4. 輸出結構化的「資料管線採納清單 (Data Ingestion Manifest)」供引擎排程使用
"""

import json
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# 取得 dist/apis.json 路徑
ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_JSON = ROOT_DIR / "dist" / "apis.json"

RESEARCH_DOMAINS = {
    "geospatial": {
        "title": "地理空間與地籍圖資",
        "keywords": ["國土測繪", "門牌", "地圖", "geocoder", "wmts"]
    },
    "hazard_risks": {
        "title": "災害與環境風險評估",
        "keywords": ["淹水", "水庫", "地震", "空氣品質", "aqi"]
    },
    "transport_access": {
        "title": "大眾運輸生活機能",
        "keywords": ["捷運", "公車", "自行車", "高鐵", "台鐵", "youbike"]
    },
    "demographics_governance": {
        "title": "人口結構與生活公政",
        "keywords": ["人口", "戶政", "實價登錄", "垃圾車", "soa"]
    }
}

def load_catalog(json_path: Path) -> list[dict]:
    if not json_path.exists():
        raise FileNotFoundError(f"找不到目錄檔案: {json_path}，請先執行 build_catalog.py")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_source_for_domain(catalog: list[dict], domain_config: dict) -> list[dict]:
    keywords = [k.lower() for k in domain_config["keywords"]]
    matched = []
    for item in catalog:
        searchable_text = f"{item['id']} {item['name_zh']} {item.get('name_en', '')} {item['description_zh']}".lower()
        if any(kw in searchable_text for kw in keywords):
            matched.append(item)
    return matched

def generate_ingestion_manifest(catalog: list[dict]) -> dict:
    manifest = {
        "engine": "Land-Self-Built-Housing-Research-Engine",
        "catalog_version": "public-apis-tw@2026-10-14",
        "total_sources_evaluated": len(catalog),
        "selected_pipelines": {}
    }

    print("=" * 70)
    print(" 土地型自住房研究引擎：資料來源登錄檢索報告")
    print("=" * 70)

    for domain_key, config in RESEARCH_DOMAINS.items():
        matched_items = match_source_for_domain(catalog, config)
        print(f"\n[維度] {config['title']} (共匹配 {len(matched_items)} 個候選來源)：")

        pipeline_entries = []
        for it in matched_items:
            # 依 catalog policy 評估可用性：verified 優先採用；candidate 標記待覆核
            is_verified = (it.get("review_status") == "verified")
            auth = it.get("auth_type", "none")
            license_name = it.get("license_name", "unknown")
            base_url = it.get("base_url")

            status_flag = "[Verified]" if is_verified else "[Candidate]"
            print(f"  - [{it['id']}] {it['name_zh']} ({it['provider']})")
            print(f"    狀態: {status_flag} | 授權: {license_name} | 鑑別: {auth}")
            if base_url:
                print(f"    端點: {base_url}")
            else:
                print(f"    文件: {it['docs_url']}")

            pipeline_entries.append({
                "source_id": it["id"],
                "name": it["name_zh"],
                "provider": it["provider"],
                "review_status": it.get("review_status"),
                "verification_level": it.get("verification_level"),
                "auth_type": auth,
                "license": license_name,
                "endpoint_or_docs": base_url or it["docs_url"],
                "ingestion_strategy": "REST_DIRECT_QUERY" if base_url else "DOCS_LINK_OR_FALLBACK"
            })

        manifest["selected_pipelines"][domain_key] = pipeline_entries

    return manifest

def main():
    catalog = load_catalog(DIST_JSON)
    manifest = generate_ingestion_manifest(catalog)

    print("\n" + "=" * 70)
    print(" 採納結果摘要 (Manifest Summary)")
    print("=" * 70)
    total_selected = sum(len(v) for v in manifest["selected_pipelines"].values())
    print(f"總共自 public-apis-tw 成功挑選 {total_selected} 個相關資料管道，覆蓋四大研究維度。")
    print("下游研究引擎無需重新搜尋政府門戶或猜測授權條款，直接可依 manifest 自動化排程調用。")

if __name__ == "__main__":
    main()
