import json
from pathlib import Path
import pytest
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from scan_data_gov_tw import (
    is_pure_static_url,
    extract_valid_api_urls,
    evaluate_dataset,
    run_scanner,
    build_candidate_entry
)
from validate_catalog import validate_entry

FIXTURE_FILE = ROOT / "tests" / "fixtures" / "sample_datagov_datasets.json"

def test_is_pure_static_url():
    """確認純靜態檔案副檔名與下載路徑能被準確識別"""
    # 靜態檔案
    assert is_pure_static_url("https://example.com/data.csv") is True
    assert is_pure_static_url("https://example.com/export.xlsx") is True
    assert is_pure_static_url("https://example.com/archive.zip") is True
    assert is_pure_static_url("https://apiservice.mol.gov.tw/odservice/download/12345") is True
    assert is_pure_static_url("https://tcgbusfs.blob.core.windows.net/dotapp/youbike.json") is True
    assert is_pure_static_url("https://stats.moe.gov.tw/files/opendata/base2.json") is True

    # 真實 API 端點
    assert is_pure_static_url("https://opendata.immigration.gov.tw/APIS/TPE11") is False
    assert is_pure_static_url("https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J") is False
    assert is_pure_static_url("https://tpapim-es.twport.com.tw:8065/v1.0/TcsNetOpenApi/GetForecastData?fid=71") is False

def test_extract_valid_api_urls():
    """確認能從混合 URL 中剔除靜態下載、保留真實 API 端點"""
    item = {
        "all_url": [
            "https://apiservice.mol.gov.tw/OdService/download/A17000000J-020057-FyT",
            "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-020057-Nvt"
        ]
    }
    extracted = extract_valid_api_urls(item)
    assert len(extracted) == 1
    assert extracted[0] == "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-020057-Nvt"

def test_evaluate_dataset_rejects_pure_static_records():
    """純檔案記錄經 evaluate_dataset 評估應回傳 None (過濾淘汰)"""
    static_item = {
        "nid": 6239,
        "title": "純靜態檔案資料",
        "all_url": ["https://stats.moe.gov.tw/files/opendata/base2.csv"],
        "all_oas_url": None,
        "api_doc_url": []
    }
    assert evaluate_dataset(static_item) is None

def test_evaluate_dataset_accepts_valid_api():
    """具備真實 API 介面的資料集應通過評估並提取出端點資訊"""
    api_item = {
        "nid": 167537,
        "title": "桃園機場第一航廈入境人次預報",
        "agency_name": "內政部移民署",
        "all_url": ["https://opendata.immigration.gov.tw/APIS/TPE11"],
        "all_oas_url": None,
        "api_doc_url": []
    }
    result = evaluate_dataset(api_item)
    assert result is not None
    assert result["nid"] == "167537"
    assert len(result["valid_endpoints"]) == 1

def test_scanner_end_to_end_with_fixture():
    """從 Fixture 執行端到端掃描，斷言過濾比率與產出項目的 Schema 合規性"""
    assert FIXTURE_FILE.exists()
    
    entries = run_scanner(fixture_path=FIXTURE_FILE, dry_run=True, ignore_existing=True)
    
    # Fixture 中共 5 筆，其中 2 筆為純檔案 (6239, 137993)，應被過濾；留下 3 筆真實 API
    assert len(entries) == 3
    found_nids = [e["website_url"].split("/")[-1] for e in entries]
    assert "6239" not in found_nids, "純檔案 6239 不應出現在候選清單中"
    assert "137993" not in found_nids, "純 blob dump 137993 不應出現在候選清單中"
    assert "167537" in found_nids
    assert "161479" in found_nids
    assert "6624" in found_nids

    # 驗證動態產生的每一筆 candidate 均 100% 符合 Catalog Schema
    for entry in entries:
        errors, warnings = validate_entry(entry, expected_id=entry["id"])
        assert errors == [], f"動態產生的候選項目 {entry['id']} 未通過 Schema 驗證: {errors}"
        assert entry["review_status"] == "candidate"
        assert entry["verification_level"] == "none"
        # 關鍵驗證：未經實地探測與規格審查的欄位必須為 unknown，絕不盲目猜測
        assert entry["service_status"] == "unknown", "候選條目不可未經探測宣稱 active"
        assert entry["auth_type"] in ("unknown", "api_key")
        assert "sources" in entry and len(entry["sources"]) >= 1

def test_scanner_deduplication_by_nid_and_endpoint():
    """確認已在目錄中收錄的來源 NID 與端點不會被重複生成 candidate"""
    from scan_data_gov_tw import cluster_and_filter

    item = {
        "nid": "167537",
        "title": "桃園機場第一航廈入境人次預報",
        "agency": "內政部移民署",
        "valid_endpoints": ["https://opendata.immigration.gov.tw/APIS/TPE11"]
    }
    
    # 情境 1: NID 已經在既有目錄指紋中
    filtered, skipped = cluster_and_filter(
        [item],
        existing_ids=set(),
        existing_nids={"167537"},
        existing_endpoints=set()
    )
    assert len(filtered) == 0
    assert len(skipped) == 1
    assert "NID 167537 已於既有目錄收錄" in skipped[0]["reason"]

    # 情境 2: 端點 URL 已經在既有目錄指紋中
    filtered_ep, skipped_ep = cluster_and_filter(
        [item],
        existing_ids=set(),
        existing_nids=set(),
        existing_endpoints={"https://opendata.immigration.gov.tw/apis/tpe11"}
    )
    assert len(filtered_ep) == 0
    assert len(skipped_ep) == 1
    assert "端點 URL 已於既有目錄收錄" in skipped_ep[0]["reason"]

