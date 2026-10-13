#!/usr/bin/env python3
"""
scan_data_gov_tw.py - data.gov.tw 自動 API 掃描與候選草稿生成器

流程：
1. 查詢資料開放平臺搜尋介面 (POST https://data.gov.tw/api/front/dataset/list)
   - 支援 category_dataset_tid: 43095 (API服務 / OpenAPI)
   - 支援 all_file_format_tid: 11519 (API 格式)
   - 支援 all_file_format_tid: 6413 (WEBSERVICES 格式)
   - 支援 all_file_format_tid: 6410 (JSON 格式熱門項目)
2. 過濾純靜態檔案 (CSV, XLSX, ZIP, 靜態 dump, blob 下載點)
3. 提取可程式化端點與 Swagger/OpenAPI 定義
4. 多維度去重（比對既有 ID、資料集 NID 來源與端點 URL，避免重複建立）
5. 排除已於目錄中完整收錄之大型整合領域 (TDX, CWA, MOENV, WRA)
6. 誠實記錄未經確認的欄位為 unknown (避免把未知當確定)
7. 動態產生符合 schemas/api.schema.json 的 candidate YAML 條目草稿
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import time
import urllib.request
import urllib.parse
import yaml

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_APIS_DIR = ROOT_DIR / "data" / "apis"

LIST_API = "https://data.gov.tw/api/front/dataset/list"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Content-Type": "application/json"
}

def is_pure_static_url(url: str) -> bool:
    """判斷單一 URL 是否為純靜態檔案下載或 dump"""
    if not url or not url.startswith("http"):
        return True
    u_lower = url.lower()
    clean_path = u_lower.split("?")[0]

    # 常見靜態副檔名 (若無動態查詢參數或只是 download 呼叫)
    static_exts = ('.csv', '.xlsx', '.xls', '.zip', '.pdf', '.ods', '.7z', '.rar', '.txt', '.doc', '.docx')
    if any(clean_path.endswith(ext) for ext in static_exts):
        if "?" not in url or "download" in u_lower:
            return True

    # 常見純檔案下載伺服器與路徑特徵
    static_markers = [
        "apiservice.mol.gov.tw/odservice/download",
        "/api/dataset/",  # 如 data.taipei 的 /download 封裝
        "/api/datasets/", # 如 data.ntpc 的 /csv/file
        "blob.core.windows.net",
        "stats.moe.gov.tw/files/opendata/",
        "od.cdc.gov.tw/eic/",
        "/resource.download"
    ]
    if any(m in u_lower for m in static_markers) and ("/rest/datastore" not in u_lower and "/apis/" not in u_lower):
        return True

    return False

def extract_valid_api_urls(dataset_item: dict) -> list[str]:
    """從資料集的 all_url 列表中提取真正具有程式化介面特徵的端點"""
    endpoints = []
    urls = dataset_item.get("all_url", [])
    if isinstance(urls, str):
        urls = [urls]

    for u in urls:
        if not u or not u.startswith("http"):
            continue
        if is_pure_static_url(u):
            continue

        u_lower = u.lower()
        # API 特徵
        api_features = [
            "/rest/datastore", "/apis/", "/api/v", "swagger", "openapi",
            "getforecastdata", "odata", "%24format=", "$format=", "format=json",
            "authorization=", "apikey=", "api_key="
        ]
        if any(feat in u_lower for feat in api_features):
            endpoints.append(u)
        elif "/api/" in u_lower and not any(clean_u.endswith(ext) for clean_u in [u_lower.split("?")[0]] for ext in ('.csv', '.zip', '.xlsx')):
            endpoints.append(u)

    return endpoints

def map_category(agency: str, title: str) -> str:
    """依機關名稱與標題文字映射至 schema 定義的主要業務領域"""
    text = (agency + " " + title).lower()
    if any(k in text for k in ["氣象", "天氣", "雨量", "地震", "空氣", "水利", "淹水", "水庫", "河川", "環境"]):
        return "Weather & Environment"
    if any(k in text for k in ["交通", "鐵路", "客運", "公車", "捷運", "自行車", "航班", "港", "船舶", "航空", "車輛", "動態"]):
        return "Transportation"
    if any(k in text for k in ["金融", "股票", "匯率", "商業", "公司", "發票", "稅", "財政", "基金"]):
        return "Finance & Business"
    if any(k in text for k in ["地圖", "國土", "測繪", "坐標", "地籍", "門牌", "空間"]):
        return "Maps & Geospatial"
    if any(k in text for k in ["醫療", "健保", "健康", "疾病", "衛生", "醫事", "藥品"]):
        return "Healthcare & Public Health"
    if any(k in text for k in ["觀光", "旅遊", "文化", "藝文", "景點", "古蹟"]):
        return "Culture & Tourism"
    if any(k in text for k in ["教育", "學術", "學校", "研考", "專利", "研究", "ttqs"]):
        return "Education & Research"
    if any(k in text for k in ["工具", "郵遞區號", "轉換"]):
        return "Developer Tools"
    return "Government & Public Services"

def clean_description(desc: str, title: str) -> str:
    """清理摘要字串，確保長度與客觀性"""
    if not desc or len(desc.strip()) < 5:
        return f"由主管機關提供之{title}資料查詢介面與程式化端點。"
    clean = re.sub(r'<[^>]+>', '', desc).replace("\r\n", " ").replace("\n", " ").strip()
    if len(clean) < 5:
        return f"由主管機關提供之{title}資料查詢介面與程式化端點。"
    return clean[:300]

def slugify(text: str) -> str:
    """將文字轉為符合 schema 正則 (^[a-z0-9]+(-[a-z0-9]+)*$) 的 slug"""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    slug = re.sub(r"-+", "-", slug)
    return slug or "unknown-service"

def parse_existing_catalog_fingerprints(data_dir: Path) -> tuple[set[str], set[str], set[str]]:
    """
    從既有目錄讀取指紋：
    1. existing_ids: 既有 ID 集合
    2. existing_nids: 既有收錄來源中的 data.gov.tw NID 集合
    3. existing_endpoints: 既有收錄的端點與文件 URL 集合
    """
    existing_ids: set[str] = set()
    existing_nids: set[str] = set()
    existing_endpoints: set[str] = set()

    if not data_dir.exists():
        return existing_ids, existing_nids, existing_endpoints

    for yf in data_dir.glob("*.yml"):
        existing_ids.add(yf.stem)
        try:
            with open(yf, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
                if not isinstance(d, dict):
                    continue
                # 擷取 sources 與 website_url 中的 nid
                all_links = d.get("sources", []) + [d.get("website_url", ""), d.get("docs_url", "")]
                for link in all_links:
                    if link and isinstance(link, str):
                        m = re.search(r"data\.gov\.tw/dataset/(\d+)", link)
                        if m:
                            existing_nids.add(m.group(1))
                        existing_endpoints.add(link.rstrip("/").lower())

                base = d.get("base_url")
                if base and isinstance(base, str):
                    existing_endpoints.add(base.rstrip("/").lower())
        except Exception:
            pass

    return existing_ids, existing_nids, existing_endpoints

def fetch_datasets_from_api(
    filter_field: str,
    query_val: str,
    page_limit: int = 100,
    max_pages: int = 5,
    sleep_sec: float = 0.2
) -> list[dict]:
    """向 data.gov.tw 搜尋 API 發送分頁查詢"""
    results = []
    for page in range(1, max_pages + 1):
        payload = {
            "bool": [],
            "filter": [{"fields": filter_field, "query": str(query_val)}],
            "page_num": page,
            "page_limit": page_limit,
            "sort": "resource_download_times_past_7days_desc"
        }
        req = urllib.request.Request(LIST_API, data=json.dumps(payload).encode('utf-8'), headers=DEFAULT_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                items = data.get("payload", {}).get("search_result", [])
                total = data.get("payload", {}).get("search_count", 0)
                if not items:
                    break
                results.extend(items)
                print(f"  [{filter_field}:{query_val}] Page {page}: 取得 {len(items)} 筆 (累積: {len(results)}/{total})")
                if len(results) >= total:
                    break
            time.sleep(sleep_sec)
        except Exception as e:
            print(f"  [!] 擷取 {filter_field}:{query_val} 第 {page} 頁時發生錯誤: {e}", file=sys.stderr)
            break
    return results

def evaluate_dataset(item: dict) -> dict | None:
    """
    評估單一資料集是否符合可程式化 API 標準。
    若符合，回傳分析結果；若為純檔案，回傳 None。
    """
    nid = item.get("nid")
    title = (item.get("title") or "").strip()
    agency = (item.get("agency_name") or "").strip()
    all_oas = item.get("all_oas_url")
    if all_oas and not all_oas.startswith("http"):
        all_oas = None

    raw_docs = item.get("api_doc_url", [])
    if isinstance(raw_docs, str):
        raw_docs = [raw_docs]
    docs = [d for d in raw_docs if d and isinstance(d, str) and d.startswith("http")]

    valid_endpoints = extract_valid_api_urls(item)

    # 判定條件：必須有 OAS，或有有效文件網址，或有提取出的 API 端點
    if not all_oas and not docs and not valid_endpoints:
        return None

    return {
        "raw": item,
        "nid": str(nid),
        "title": title,
        "agency": agency,
        "all_oas_url": all_oas,
        "docs_urls": docs,
        "valid_endpoints": valid_endpoints
    }

def build_candidate_entry(eval_result: dict, today_str: str | None = None) -> dict:
    """
    動態從評估結果組裝符合 Schema 規範的 Candidate YAML 條目字典。
    嚴格準則：未經人工驗證或缺乏明確規格之欄位，一律填寫 'unknown'，絕不假裝已知。
    """
    raw = eval_result["raw"]
    nid = eval_result["nid"]
    title = eval_result["title"]
    agency = eval_result["agency"]
    all_oas = eval_result["all_oas_url"]
    docs = eval_result["docs_urls"]
    endpoints = eval_result["valid_endpoints"]

    today = today_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cat = map_category(agency, title)
    desc = clean_description(raw.get("field_description") or raw.get("abstract") or "", title)

    # 優先選取 docs_url
    docs_url = docs[0] if docs else (all_oas if all_oas else f"https://data.gov.tw/dataset/{nid}")
    base_url = endpoints[0] if endpoints else None
    https_support = "yes" if (base_url and base_url.startswith("https")) or (docs_url and docs_url.startswith("https")) else "no"

    # 1. 授權與商用推論 (避免默認 OGDL)
    raw_license = (raw.get("license_name") or raw.get("license") or "").strip()
    if "政府資料開放授權條款" in raw_license or "OGDL" in raw_license:
        license_name = "OGDL-Taiwan-1.0"
        commercial_use = "allowed"
    elif raw_license:
        license_name = raw_license
        commercial_use = "unknown"
    else:
        license_name = "unknown"
        commercial_use = "unknown"

    # 2. 認證機制 (避免默認 none)
    all_endpoints_str = " ".join(endpoints).lower()
    if any(k in all_endpoints_str for k in ["authorization=", "apikey=", "api_key="]):
        auth_type = "api_key"
    else:
        # 沒有抓到明確認證資訊不等於免認證，保留 unknown
        auth_type = "unknown"

    # 3. 費用層級 (避免默認 free)
    raw_charge = (raw.get("charge") or "").strip()
    if "免費" in raw_charge:
        access_tier = "free"
    elif raw_charge:
        access_tier = "unknown"
    else:
        access_tier = "unknown"

    # 4. 架構風格 (避免默認 REST)
    if all_oas or any("swagger" in d.lower() or "openapi" in d.lower() for d in docs):
        api_style = "REST"
        spec_formats = ["OpenAPI"]
    elif any("asmx" in u.lower() or "wsdl" in u.lower() for u in endpoints):
        api_style = "SOAP"
        spec_formats = ["WSDL"]
    else:
        api_style = "unknown"
        spec_formats = []

    # 動態產生 slug
    slug = f"gov-tw-nid-{nid}"

    entry = {
        "id": slug,
        "name_zh": title,
        "description_zh": desc,
        "category": cat,
        "provider": agency or "政府機關",
        "provider_type": "official",
        "docs_url": docs_url,
        "website_url": f"https://data.gov.tw/dataset/{nid}",
        "api_style": api_style,
        "auth_type": auth_type,
        "access_tier": access_tier,
        "https_support": https_support,
        "cors_support": "unknown",
        "license_name": license_name,
        "commercial_use": commercial_use,
        "service_status": "unknown",  # 未經端點探測前不宣稱 active
        "review_status": "candidate",
        "verification_level": "none",
        "last_reviewed_at": today,
        "sources": [
            f"https://data.gov.tw/dataset/{nid}"
        ],
        "notes": f"由 data.gov.tw 掃描器自動動態發現與轉換之候選草稿 (nid: {nid})。發現時間：{today}。各項技術指標均待人工實地核實。"
    }
    if base_url:
        entry["base_url"] = base_url
    if spec_formats:
        entry["spec_formats"] = spec_formats

    return entry

def cluster_and_filter(
    evaluated_items: list[dict],
    existing_ids: set[str],
    existing_nids: set[str],
    existing_endpoints: set[str],
    skip_large_platforms: bool = True
) -> tuple[list[dict], list[dict]]:
    """
    對掃描評估結果進行去重與智慧分群：
    1. 實作多維度去重（排除已收錄之 ID、已收錄之來源 NID、已收錄之端點 URL）
    2. 排除已於策略 A 細粒度收錄之大型垂直平台 (TDX, CWA, MOENV, WRA)
    3. 對於同質性極高之 Datastore (如勞動部)，動態按業務單位分群，每群僅保留最具代表性/下載量高之端點
    回傳 (通過篩選之候選項目, 被去重剔除之項目)
    """
    filtered = []
    skipped_duplicates = []
    mol_items = []

    for item in evaluated_items:
        nid = str(item["nid"])
        str_all = f"{item['title']} {item['agency']} {item.get('all_oas_url', '')} {' '.join(item['valid_endpoints'])}".lower()

        # 1. 檢查來源 NID 是否已收錄
        if nid in existing_nids:
            skipped_duplicates.append({"item": item, "reason": f"NID {nid} 已於既有目錄收錄"})
            continue

        # 2. 檢查端點或文件 URL 是否已於既有目錄收錄
        item_links = [u.rstrip("/").lower() for u in item["valid_endpoints"]]
        if any(link in existing_endpoints for link in item_links):
            skipped_duplicates.append({"item": item, "reason": "端點 URL 已於既有目錄收錄"})
            continue

        # 3. 排除已於策略 A 細粒度收錄之大型垂直平台
        if skip_large_platforms:
            if any(p in str_all for p in ["transportdata.tw", "cwa.gov.tw", "氣象署", "moenv.gov.tw", "wra.gov.tw"]):
                continue

        # 4. 勞動部 Datastore 收集待聚類
        if "apiservice.mol.gov.tw" in str_all or "勞動部" in item["agency"]:
            mol_items.append(item)
            continue

        # 5. 檢查預期 slug 是否與既有 ID 碰撞
        candidate_slug = f"gov-tw-nid-{nid}"
        if candidate_slug in existing_ids:
            skipped_duplicates.append({"item": item, "reason": f"ID {candidate_slug} 已存在"})
            continue

        filtered.append(item)

    # 針對勞動部 Datastore 進行業務子機關分群代表性提取
    if mol_items:
        agency_groups = {}
        for it in mol_items:
            sub_ag = it["agency"] or "勞動部"
            agency_groups.setdefault(sub_ag, []).append(it)
        
        # 每個業務子機關依下載次數動態選取前 1~2 筆代表
        for sub_ag, group in agency_groups.items():
            sorted_group = sorted(
                group,
                key=lambda x: x["raw"].get("resource_download_times_past_7days", 0) or 0,
                reverse=True
            )
            for cand in sorted_group[:2]:
                cand_slug = f"gov-tw-nid-{cand['nid']}"
                if cand_slug not in existing_ids and cand["nid"] not in existing_nids:
                    filtered.append(cand)

    return filtered, skipped_duplicates

def run_scanner(
    fixture_path: Path | None = None,
    out_dir: Path | None = None,
    dry_run: bool = False,
    max_pages: int = 3,
    ignore_existing: bool = False
) -> list[dict]:
    """執行完整掃描流程"""
    target_out_dir = out_dir or DATA_APIS_DIR
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 讀取既有目錄指紋（ID、NID 與端點集合）
    if ignore_existing:
        existing_ids, existing_nids, existing_endpoints = set(), set(), set()
        print("[*] 略過既有目錄指紋比對 (ignore_existing=True)")
    else:
        existing_ids, existing_nids, existing_endpoints = parse_existing_catalog_fingerprints(target_out_dir)
        print(f"[*] 既有目錄指紋解析完成: {len(existing_ids)} 個 ID, {len(existing_nids)} 個來源 NID, {len(existing_endpoints)} 個端點/文件連結")

    raw_datasets = []
    if fixture_path and fixture_path.exists():
        print(f"[*] 使用本地測試 Fixture: {fixture_path}")
        with open(fixture_path, "r", encoding="utf-8") as f:
            raw_datasets = json.load(f)
    else:
        print("[*] 正在向 data.gov.tw 發送分頁查詢 (API服務/WEBSERVICES/API格式/JSON熱門)...")
        # 1. 官方 API服務
        raw_datasets.extend(fetch_datasets_from_api("category_dataset_tid", "43095", max_pages=max_pages))
        # 2. 官方 API 格式
        raw_datasets.extend(fetch_datasets_from_api("all_file_format_tid", "11519", max_pages=max_pages))
        # 3. 官方 WEBSERVICES
        raw_datasets.extend(fetch_datasets_from_api("all_file_format_tid", "6413", max_pages=max_pages))
        # 4. JSON 格式熱門
        raw_datasets.extend(fetch_datasets_from_api("all_file_format_tid", "6410", max_pages=max_pages))

    # 去重
    unique_items = {}
    for d in raw_datasets:
        nid = str(d.get("nid"))
        if nid and nid not in unique_items:
            unique_items[nid] = d

    print(f"[*] 掃描取得唯一資料集共: {len(unique_items)} 筆")

    # 評估與過濾純檔案
    evaluated_candidates = []
    static_filtered_count = 0
    for nid, d in unique_items.items():
        res = evaluate_dataset(d)
        if res is not None:
            evaluated_candidates.append(res)
        else:
            static_filtered_count += 1

    print(f"[*] 過濾純靜態檔案與 dump: {static_filtered_count} 筆")
    print(f"[*] 符合可程式化特徵之資料集: {len(evaluated_candidates)} 筆")

    # 多維度去重與聚類
    clustered, skipped_duplicates = cluster_and_filter(
        evaluated_candidates,
        existing_ids=existing_ids,
        existing_nids=existing_nids,
        existing_endpoints=existing_endpoints
    )
    print(f"[*] 經多維度去重剔除之既有/重複條目: {len(skipped_duplicates)} 筆")
    print(f"[*] 新發現且通過聚類收斂之高品質候選項目: {len(clustered)} 筆")

    # 產出 YAML entries
    generated_entries = []
    for c in clustered:
        entry = build_candidate_entry(c, today_str=today_str)
        generated_entries.append(entry)

    if not dry_run:
        target_out_dir.mkdir(parents=True, exist_ok=True)
        for g in generated_entries:
            file_path = target_out_dir / f"{g['id']}.yml"
            # 避免覆蓋已經被人工提升為 verified 的既有檔案
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as existing_f:
                        existing_data = yaml.safe_load(existing_f)
                        if existing_data.get("review_status") == "verified":
                            continue
                except Exception:
                    pass

            with open(file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(g, f, allow_unicode=True, sort_keys=False)
            print(f"  + [Candidate 新增] {g['id']} ({g['name_zh']}) -> {file_path.name}")

    return generated_entries

def main():
    parser = argparse.ArgumentParser(description="data.gov.tw 自動 API 掃描與候選草稿生成器")
    parser.add_argument("--fixture", type=Path, help="從本地 JSON Fixture 載入資料集進行測試")
    parser.add_argument("--dry-run", action="store_true", help="僅執行掃描與分析，不寫入檔案")
    parser.add_argument("--out-dir", type=Path, help="指定 YAML 輸出目錄")
    parser.add_argument("--max-pages", type=int, default=2, help="每個類別最大抓取分頁數")
    args = parser.parse_args()

    entries = run_scanner(
        fixture_path=args.fixture,
        out_dir=args.out_dir,
        dry_run=args.dry_run,
        max_pages=args.max_pages
    )
    print(f"\n[V] 掃描作業完成，共產出/發現 {len(entries)} 筆候選項目。")

if __name__ == "__main__":
    main()
