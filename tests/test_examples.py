from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "examples"))

from real_estate_research_consumer import (
    load_catalog,
    match_source_for_domain,
    generate_ingestion_manifest,
    RESEARCH_DOMAINS
)

def test_real_estate_research_consumer_logic():
    """直接調用下游整合邏輯，驗證目錄解析、主題匹配與 Manifest 產出"""
    dist_json = ROOT / "dist" / "apis.json"
    assert dist_json.exists(), "dist/apis.json 必須存在"

    catalog = load_catalog(dist_json)
    assert len(catalog) >= 50, f"目錄資料量應至少 50 筆，實際取得: {len(catalog)}"

    manifest = generate_ingestion_manifest(catalog)
    assert manifest["engine"] == "Land-Self-Built-Housing-Research-Engine"
    assert manifest["total_sources_evaluated"] == len(catalog)

    pipelines = manifest["selected_pipelines"]
    # 斷言四大研究維度皆有匹配到合適的資料來源管道
    for domain_key in RESEARCH_DOMAINS.keys():
        assert domain_key in pipelines, f"缺少維度: {domain_key}"
        assert len(pipelines[domain_key]) > 0, f"維度 {domain_key} 應至少匹配一個來源"

    # 檢查地籍空間維度包含 NLSC WMTS 或 TGOS
    geo_sources = [item["source_id"] for item in pipelines["geospatial"]]
    assert "nlsc-map-api" in geo_sources or "tgos-geocoder" in geo_sources

    # 檢查災害風險維度包含水情或地震或 AQI
    hazard_sources = [item["source_id"] for item in pipelines["hazard_risks"]]
    assert any("wra" in s or "cwa" in s or "moenv" in s for s in hazard_sources)
