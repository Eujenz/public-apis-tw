#!/usr/bin/env python3
"""
scrape_api_docs.py - 使用 Crawlee (Playwright) 爬取與探測 API 官方文件

功能特性：
1. 支援 SPA / JavaScript 動態渲染網頁（如 Swagger UI, Redoc, React/Vue Portal）
2. 網路封包監聽 (Network Interception)：自動捕獲頁面發出的 OpenAPI / Swagger JSON 規格
3. 自動將解析成果轉換為符合 public-apis-tw 規範之 YAML 條目草稿
4. 匯出原始 OpenAPI/Swagger JSON 供深入分析
"""

import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

import yaml

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "apis"

def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "unknown-api"

def infer_auth_type(spec: dict) -> str:
    """從 OpenAPI / Swagger 規格中推斷身份驗證類型"""
    security_defs = spec.get("securityDefinitions") or spec.get("components", {}).get("securitySchemes", {})
    if not security_defs:
        return "none"
    
    types = []
    for s_name, s_val in security_defs.items():
        stype = s_val.get("type", "").lower()
        if stype in ("apikey", "api_key"):
            types.append("api_key")
        elif stype in ("oauth2", "oauth", "openidconnect"):
            types.append("oauth")
        elif stype == "http":
            scheme = s_val.get("scheme", "").lower()
            if scheme == "bearer":
                types.append("api_key")
            else:
                types.append("other")
        else:
            types.append("other")
    
    if "api_key" in types:
        return "api_key"
    if "oauth" in types:
        return "oauth"
    if types:
        return types[0]
    return "unknown"

def infer_formats(spec: dict) -> list[str]:
    formats = set()
    produces = spec.get("produces", [])
    consumes = spec.get("consumes", [])
    all_types = " ".join(produces + consumes).lower()
    if "json" in all_types:
        formats.add("JSON")
    if "xml" in all_types:
        formats.add("XML")
    if not formats:
        formats.add("JSON")
    return sorted(list(formats))

def extract_base_url(spec: dict, doc_url: str) -> str:
    # OpenAPI 3.x
    servers = spec.get("servers", [])
    if servers and isinstance(servers, list):
        first_url = servers[0].get("url", "")
        if first_url.startswith("http"):
            return first_url
        parsed = urlparse(doc_url)
        return f"{parsed.scheme}://{parsed.netloc}{first_url}".rstrip("/")

    # Swagger 2.0
    host = spec.get("host")
    base_path = spec.get("basePath", "")
    schemes = spec.get("schemes", ["https"])
    if host:
        scheme = schemes[0] if schemes else "https"
        return f"{scheme}://{host}{base_path}".rstrip("/")

    parsed = urlparse(doc_url)
    return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")

async def run_scraper(target_url: str, headless: bool = True, timeout_sec: int = 40):
    try:
        from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
        from crawlee.configuration import Configuration
    except ImportError:
        print("[!] 錯誤: 未安裝 crawlee 或 playwright 套件。")
        print("    請先執行:")
        print("      uv sync --group scraper")
        print("      uv run --group scraper playwright install chromium")
        sys.exit(1)

    captured_specs = []
    page_metadata = {}

    crawler = PlaywrightCrawler(
        headless=headless,
        request_handler_timeout=timedelta(seconds=timeout_sec),
        max_requests_per_crawl=1,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f"Navigating to {context.request.url}...")
        page = context.page

        # 監聽網路回應，攔截 Swagger / OpenAPI JSON 規格
        async def on_response(response):
            content_type = response.headers.get("content-type", "").lower()
            url_lower = response.url.lower()
            is_json_candidate = (
                "json" in content_type or
                "swagger" in url_lower or
                "openapi" in url_lower or
                "api-docs" in url_lower
            )

            if is_json_candidate:
                try:
                    data = await response.json()
                    if isinstance(data, dict) and ("swagger" in data or "openapi" in data or "paths" in data):
                        context.log.info(f"[+] 成功捕獲 OpenAPI/Swagger 規格: {response.url}")
                        captured_specs.append({
                            "url": response.url,
                            "data": data
                        })
                except Exception:
                    pass

        page.on("response", on_response)

        # 前往目標頁面並等待網路空閒
        await page.goto(context.request.url, wait_until="networkidle", timeout=timeout_sec * 1000)
        # 稍作等待以確保 client-side 腳本與 Swagger UI 渲染完畢
        await page.wait_for_timeout(3000)

        # 抓取基本頁面中繼資料備用
        title = await page.title()
        meta_desc = ""
        meta_tag = await page.query_selector('meta[name="description"]')
        if meta_tag:
            meta_desc = await meta_tag.get_attribute("content") or ""

        page_metadata["title"] = title
        page_metadata["description"] = meta_desc
        page_metadata["url"] = context.request.url

    await crawler.run([target_url])
    return captured_specs, page_metadata

def build_entry_yaml(doc_url: str, captured_specs: list, page_metadata: dict, api_id: str | None = None) -> dict:
    today_str = datetime.now().strftime("%Y-%m-%d")
    parsed_url = urlparse(doc_url)
    default_website = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if captured_specs:
        spec_data = captured_specs[0]["data"]
        info = spec_data.get("info", {})
        title = info.get("title") or page_metadata.get("title") or "未命名 API"
        raw_desc = info.get("description") or page_metadata.get("description") or "提供相關業務領域之可程式化查詢介面。"
        desc = re.sub(r"<[^>]+>", " ", raw_desc)
        desc = re.sub(r"\s+", " ", desc).strip()[:300]
        
        spec_version = "Swagger 2.0" if "swagger" in spec_data else "OpenAPI 3.0"
        auth_type = infer_auth_type(spec_data)
        data_formats = infer_formats(spec_data)
        base_url = extract_base_url(spec_data, doc_url)
        path_count = len(spec_data.get("paths", {}))
        notes = f"自動擷取自 {doc_url}。偵測到 {path_count} 個端點路徑。"
    else:
        title = page_metadata.get("title") or "未命名 API"
        desc = page_metadata.get("description") or "提供相關業務領域之可程式化查詢介面。"
        spec_version = "unknown"
        auth_type = "unknown"
        data_formats = ["JSON"]
        base_url = default_website
        notes = f"透過 Playwright 抓取頁面中繼資料，未偵測到底層 OpenAPI JSON 規格。"

    slug = api_id or slugify(title.split("-")[0].split("|")[0])

    entry = {
        "id": slug,
        "name_zh": title.strip(),
        "name_en": slug.replace("-", " ").title(),
        "description_zh": desc.strip(),
        "category": "Other",
        "provider": parsed_url.netloc,
        "provider_type": "official" if ("gov.tw" in parsed_url.netloc or "org.tw" in parsed_url.netloc) else "third_party",
        "docs_url": doc_url,
        "website_url": default_website,
        "base_url": base_url,
        "api_style": "REST",
        "spec_formats": [spec_version] if spec_version != "unknown" else [],
        "data_formats": data_formats,
        "auth_type": auth_type,
        "access_tier": "free",
        "pricing_url": default_website,
        "https_support": "yes" if doc_url.startswith("https") else "no",
        "cors_support": "unknown",
        "license_name": "OGDL-Taiwan-1.0" if "gov.tw" in parsed_url.netloc else "unknown",
        "commercial_use": "allowed" if "gov.tw" in parsed_url.netloc else "unknown",
        "service_status": "active",
        "review_status": "candidate",
        "verification_level": "docs_reviewed",
        "last_reviewed_at": today_str,
        "sources": [doc_url],
        "notes": notes,
    }
    return entry

def main():
    parser = argparse.ArgumentParser(description="使用 Crawlee 探測與擷取 API 規格")
    parser.add_argument("--url", required=True, help="目標 API 文件網址 (例如 https://tdx.transportdata.tw/api-service/swagger)")
    parser.add_argument("--api-id", default=None, help="指定 API 識別代號 (Slug)")
    parser.add_argument("--output-yaml", default=None, help="輸出的 YAML 檔案路徑")
    parser.add_argument("--output-json", default=None, help="輸出的 OpenAPI/Swagger JSON 規格路徑")
    parser.add_argument("--no-headless", action="store_true", help="以可見視窗執行瀏覽器")
    parser.add_argument("--timeout", type=int, default=30, help="逾時秒數 (預設 30s)")

    args = parser.parse_args()

    print(f"[*] 目標網址: {args.url}")
    print(f"[*] 啟動 Crawlee PlaywrightCrawler (Headless: {not args.no_headless})...")

    specs, page_meta = asyncio.run(run_scraper(
        target_url=args.url,
        headless=not args.no_headless,
        timeout_sec=args.timeout,
    ))

    print(f"\n[*] 擷取完成！捕獲到 {len(specs)} 個 OpenAPI/Swagger 規格檔案。")

    if specs and args.output_json:
        out_json_path = Path(args.output_json)
        out_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_json_path, "w", encoding="utf-8") as fp:
            json.dump(specs[0]["data"], fp, ensure_ascii=False, indent=2)
        print(f"[+] 已儲存原始規格 JSON: {out_json_path}")

    entry = build_entry_yaml(args.url, specs, page_meta, args.api_id)

    if args.output_yaml:
        out_yaml_path = Path(args.output_yaml)
        out_yaml_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_yaml_path, "w", encoding="utf-8") as fp:
            yaml.dump(entry, fp, allow_unicode=True, sort_keys=False)
        print(f"[+] 已儲存候選 YAML 條目: {out_yaml_path}")
    else:
        print("\n--- 產出的 YAML 草稿預覽 ---")
        print(yaml.dump(entry, allow_unicode=True, sort_keys=False))

    return 0

if __name__ == "__main__":
    sys.exit(main())
