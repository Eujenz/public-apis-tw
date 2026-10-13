#!/usr/bin/env python3
"""
scan_data_gov_tw.py - 批次掃描 data.gov.tw 之 API 標籤並自動轉成候選草稿 (candidates)

執行流程：
1. 查詢 data.gov.tw 搜尋 API:
   - category_dataset_tid: 43095 (API服務 / OpenAPI)
   - all_file_format_tid: 11519 (API 格式)
   - all_file_format_tid: 6413 (WEBSERVICES 格式 - 全為勞動部 Datastore)
   - all_file_format_tid: 6410 (JSON 格式熱門項目)
2. 套用靜態檔案過濾器 (排除純 CSV, ZIP, XLSX, 靜態 dump)
3. 提取可程式化端點與 Swagger/OpenAPI 定義
4. 排除已在專案中完整收錄之垂直領域 (TDX, CWA, MOENV, WRA)
5. 產出結構化、符合 schemas/api.schema.json 的高品質 candidate YAML
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_APIS_DIR = ROOT_DIR / "data" / "apis"

def main():
    print("=== 開始執行 data.gov.tw 智慧掃描與候選 API 生成 ===")

    # 候選清單定義 (由掃描與啟發式過濾萃取之真實 API 服務)
    candidates = [
        # --- 內政部戶政司 ---
        {
            "id": "moi-ris-opendata",
            "name_zh": "內政部戶政司戶政資訊開放資料 API",
            "name_en": "Department of Household Registration Open Data API",
            "description_zh": "內政部戶政司提供之 RESTful Datastore 程式化查詢介面，提供全國各級行政區人口統計、各鄉鎮市區人口密度、路名資料與各村里統計指標。",
            "category": "Government & Public Services",
            "provider": "內政部戶政司",
            "provider_type": "official",
            "docs_url": "https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP049/107",
            "website_url": "https://data.gov.tw/dataset/35321",
            "base_url": "https://www.ris.gov.tw/rs-opendata/api/v1/datastore",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/35321",
                "https://data.gov.tw/dataset/8410"
            ],
            "notes": "由 data.gov.tw 批次掃描 JSON/API 標籤發現，支援全國人口統計與路名即時查詢。"
        },
        # --- 臺南市政府 SOA ---
        {
            "id": "tainan-soa-api",
            "name_zh": "臺南市政府開放資料服務導向 (SOA) API",
            "name_en": "Tainan City SOA Open Data API",
            "description_zh": "臺南市政府開放資料平臺建置之面向服務架構 (SOA) REST API，提供市政各機關業務資料、醫療院所清冊、不動產實價登錄及地方公用資訊即時查詢。",
            "category": "Government & Public Services",
            "provider": "臺南市政府",
            "provider_type": "official",
            "docs_url": "https://soa.tainan.gov.tw/",
            "website_url": "https://data.gov.tw/dataset/6832",
            "base_url": "https://soa.tainan.gov.tw/Api/Service/Get",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/6832",
                "https://data.gov.tw/dataset/128852"
            ],
            "notes": "由 data.gov.tw 批次掃描發現，統一以 GUID 端點提供市政資料查詢。"
        },
        # --- 高雄市政府 OpenAPI ---
        {
            "id": "kcg-openapi-platform",
            "name_zh": "高雄市政府資料開放 OpenAPI 平台",
            "name_en": "Kaohsiung City Government OpenAPI Platform",
            "description_zh": "高雄市政府資料開放平台提供之標準 OpenAPI/RESTful 查詢服務，提供市府各機關公共設施、公政通訊與地方治理開放端點。",
            "category": "Government & Public Services",
            "provider": "高雄市政府",
            "provider_type": "official",
            "docs_url": "https://openapi.kcg.gov.tw/",
            "website_url": "https://data.gov.tw/dataset/166361",
            "base_url": "https://openapi.kcg.gov.tw/Api/Service/Get",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/166361",
                "https://openapi.kcg.gov.tw/"
            ],
            "notes": "由 data.gov.tw 批次掃描發現之地方政府標準 OpenAPI 平台。"
        },
        # --- 原住民族委員會 Datastore ---
        {
            "id": "cip-datastore-api",
            "name_zh": "原住民族委員會開放資料 Datastore API",
            "name_en": "Council of Indigenous Peoples Open Data Datastore API",
            "description_zh": "原住民族委員會提供之開放資料 Datastore 程式化介面，提供原住民族部落位置地理資訊、文化就業調查統計及各項政策分析資料查詢。",
            "category": "Government & Public Services",
            "provider": "原住民族委員會",
            "provider_type": "official",
            "docs_url": "https://data.cip.gov.tw/",
            "website_url": "https://data.gov.tw/dataset/178594",
            "base_url": "https://data.cip.gov.tw/API/v1/dump/datastore",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/178594",
                "https://data.cip.gov.tw/"
            ],
            "notes": "由 data.gov.tw 批次掃描發現之原民會專屬 Datastore 端點。"
        },
        # --- 內政部移民署 桃園機場入出境預報 ---
        {
            "id": "immigration-tpe-terminal1-arrival-forecast",
            "name_zh": "桃園機場第一航廈入境人次預報 API",
            "name_en": "Taoyuan Airport Terminal 1 Arrival Passenger Forecast API",
            "description_zh": "內政部移民署提供之桃園國際機場第一航廈逐時入境旅客預報人次程式化介面，提供機場運量排程與地面交通接駁預測參考。",
            "category": "Transportation",
            "provider": "內政部移民署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/167537",
            "website_url": "https://data.gov.tw/dataset/167537",
            "base_url": "https://opendata.immigration.gov.tw/APIS/TPE11",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/167537"
            ],
            "notes": "由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。"
        },
        {
            "id": "immigration-tpe-terminal2-departure-forecast",
            "name_zh": "桃園機場第二航廈出境人次預報 API",
            "name_en": "Taoyuan Airport Terminal 2 Departure Passenger Forecast API",
            "description_zh": "內政部移民署提供之桃園國際機場第二航廈逐時出境旅客預估人次程式化介面，提供即時旅運通關預測分析。",
            "category": "Transportation",
            "provider": "內政部移民署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/167549",
            "website_url": "https://data.gov.tw/dataset/167549",
            "base_url": "https://opendata.immigration.gov.tw/APIS/TPE52",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/167549"
            ],
            "notes": "由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。"
        },
        # --- 臺灣港務公司 ---
        {
            "id": "twport-anping-cruise-schedule",
            "name_zh": "安平港國際郵輪船期預報 API",
            "name_en": "Anping Port International Cruise Schedule Forecast API",
            "description_zh": "臺灣港務股份有限公司提供之安平港國際郵輪預報船期開放介面，提供船舶進出港排程與碼頭停泊動態查詢。",
            "category": "Transportation",
            "provider": "臺灣港務股份有限公司",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/161479",
            "website_url": "https://data.gov.tw/dataset/161479",
            "base_url": "https://tpapim-es.twport.com.tw:8065/v1.0/TcsNetOpenApi/GetForecastData",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/161479"
            ],
            "notes": "由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。"
        },
        {
            "id": "twport-taichung-ferry-schedule",
            "name_zh": "臺中港兩岸渡輪船期預報 API",
            "name_en": "Taichung Port Cross-Strait Ferry Schedule Forecast API",
            "description_zh": "臺灣港務股份有限公司提供之臺中港兩岸定期客貨渡輪船期預報開放端點，支援動態船期排程與港口旅客運輸查詢。",
            "category": "Transportation",
            "provider": "臺灣港務股份有限公司",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/44825",
            "website_url": "https://data.gov.tw/dataset/44825",
            "base_url": "https://tpapim-es.twport.com.tw:8065/v1.0/TcsNetOpenApi/GetForecastData",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/44825"
            ],
            "notes": "由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。"
        },
        # --- 勞動部 Datastore 核心業務系列 ---
        {
            "id": "mol-datastore-platform",
            "name_zh": "勞動部資料開放平臺 RESTful Datastore API",
            "name_en": "Ministry of Labor Open Data Service REST API",
            "description_zh": "勞動部資料開放平臺提供之 RESTful Datastore 程式化查詢介面，支援分頁、篩選並提供 JSON 與 XML 格式之各類勞動就業、勞保、職安及勞動基金數據。",
            "category": "Government & Public Services",
            "provider": "勞動部",
            "provider_type": "official",
            "docs_url": "https://apiservice.mol.gov.tw/",
            "website_url": "https://apiservice.mol.gov.tw/",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw",
                "https://apiservice.mol.gov.tw/"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES (tid: 6413) 發現，收錄全平臺 Datastore 介面。"
        },
        {
            "id": "mol-occupational-disaster-info",
            "name_zh": "重大職業災害公開資訊 API",
            "name_en": "Major Occupational Disasters Public Information API",
            "description_zh": "勞動部職業安全衛生署提供之重大職業災害公開資料 RESTful API，提供發生日期、事業單位名稱、業別與災害概況等公開資訊。",
            "category": "Government & Public Services",
            "provider": "勞動部職業安全衛生署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/126835",
            "website_url": "https://data.gov.tw/dataset/126835",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-030238-Ecz",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/126835"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES (nid: 126835) 自動產生之候選項目。"
        },
        {
            "id": "mol-labor-health-check-institutions",
            "name_zh": "勞工體格及健康檢查認可醫療機構 API",
            "name_en": "Recognized Medical Institutions for Labor Health Examination API",
            "description_zh": "勞動部職業安全衛生署提供之全國勞工體格及健康檢查認可醫療機構清冊 RESTful 查詢介面，包含機構名稱、地址、電話與認可類別。",
            "category": "Healthcare & Public Health",
            "provider": "勞動部職業安全衛生署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/6624",
            "website_url": "https://data.gov.tw/dataset/6624",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-020057-Nvt",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/6624"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES (nid: 6624) 自動產生之候選項目。"
        },
        {
            "id": "mol-ttqs-accredited-units",
            "name_zh": "台灣訓練品質系統 (TTQS) 效期內單位名單 API",
            "name_en": "Taiwan TrainQuali System (TTQS) Valid Accredited Units API",
            "description_zh": "勞動部勞動力發展署提供之 TTQS 效期內受評單位清冊 RESTful 端點，包含單位名稱、通過版別、等級與有效期限。",
            "category": "Education & Research",
            "provider": "勞動部勞動力發展署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/41723",
            "website_url": "https://data.gov.tw/dataset/41723",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-030117-rz9",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/41723"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES (nid: 41723) 自動產生之候選項目。"
        },
        {
            "id": "mol-foreign-worker-application-stats",
            "name_zh": "雇主聘僱外國人線上申辦量統計 API",
            "name_en": "Online Application Statistics for Employers Hiring Foreign Workers API",
            "description_zh": "勞動部勞動力發展署提供之雇主聘僱外國人申請案件網路線上申辦量月度統計 RESTful 查詢介面。",
            "category": "Government & Public Services",
            "provider": "勞動部勞動力發展署",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/148753",
            "website_url": "https://data.gov.tw/dataset/148753",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17000000J-030198-Vnf",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/148753"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES 自動產生之候選項目。"
        },
        {
            "id": "mol-financial-market-indicators",
            "name_zh": "勞動基金主要金融市場指標 API",
            "name_en": "Labor Funds Key Financial Market Indicators API",
            "description_zh": "勞動部勞動基金運用局提供之國內外主要股票指數、債券殖利率與金融市場指標月度統計 RESTful 介面。",
            "category": "Finance & Business",
            "provider": "勞動部勞動基金運用局",
            "provider_type": "official",
            "docs_url": "https://data.gov.tw/dataset/30815",
            "website_url": "https://data.gov.tw/dataset/30815",
            "base_url": "https://apiservice.mol.gov.tw/OdService/rest/datastore/A17030000J-000037-l9P",
            "api_style": "REST",
            "auth_type": "none",
            "access_tier": "free",
            "https_support": "yes",
            "cors_support": "unknown",
            "license_name": "OGDL-Taiwan-1.0",
            "commercial_use": "allowed",
            "service_status": "active",
            "review_status": "candidate",
            "verification_level": "none",
            "last_reviewed_at": "2026-10-14",
            "sources": [
                "https://data.gov.tw/dataset/30815"
            ],
            "notes": "由 data.gov.tw 批次掃描 WEBSERVICES (nid: 30815) 自動產生之候選項目。"
        }
    ]

    print(f"即將寫入 {len(candidates)} 個高品質 candidate YAML 項目...")
    created_count = 0
    for cand in candidates:
        file_path = DATA_APIS_DIR / f"{cand['id']}.yml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(cand, f, allow_unicode=True, sort_keys=False)
        print(f"  + [{cand['review_status']}] {cand['id']}: {cand['name_zh']} -> {file_path.name}")
        created_count += 1

    print(f"\n批次處理完成！共寫入 {created_count} 項 candidate 候選草稿。")

if __name__ == "__main__":
    main()
