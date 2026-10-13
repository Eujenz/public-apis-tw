#!/usr/bin/env python3
"""
check_links.py - 檢查 API 目錄中官方文件與來源連結之可存取性 (可選工具)

特性：
- 友善請求間隔 (預設 0.5s)，附帶標準 User-Agent
- 支援 HEAD 請求，若伺服器回傳 405/403/501 則優雅退回 GET (串流讀取少量位元組)
- 處理 403 / 429 防火牆限制：標記為需人工確認，不逕自認定服務失效
- 僅在明確傳入參數或獨立維護時執行，CI 預設不發起大規模即時連線
"""

import sys
import time
from pathlib import Path
import yaml
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "apis"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (public-apis-tw LinkChecker; Contact: https://github.com/public-apis-tw)"
}

TIMEOUT = 8

def test_url(url: str) -> tuple[int, str]:
    try:
        # 先以 HEAD 嘗試
        res = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if res.status_code in (405, 403, 501):
            # 退回 GET 嘗試只讀取 header
            res = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True)
        return res.status_code, "OK"
    except requests.exceptions.Timeout:
        return 0, "Timeout"
    except requests.exceptions.SSLError:
        return 0, "SSL Error"
    except requests.exceptions.ConnectionError:
        return 0, "Connection Error"
    except Exception as e:
        return 0, str(e)

def main():
    yaml_files = sorted(list(DATA_DIR.glob("*.yml")) + list(DATA_DIR.glob("*.yaml")))
    print(f"[*] 開始檢查 {len(yaml_files)} 個 API 檔案之文件連結...")

    results = []
    for f in yaml_files:
        with open(f, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)

        api_id = data.get("id", f.stem)
        docs_url = data.get("docs_url")
        if not docs_url:
            continue

        print(f"  -> 測試 [{api_id}] {docs_url} ...", end=" ", flush=True)
        status_code, msg = test_url(docs_url)
        print(f"[{status_code} - {msg}]")

        results.append((api_id, docs_url, status_code, msg))
        time.sleep(0.3)

    print("\n--- 檢查摘要 ---")
    failures = [r for r in results if r[2] >= 400 or r[2] == 0]
    if failures:
        print(f"[!] 發現 {len(failures)} 個存取異常或需人工覆核的連結：")
        for api_id, url, code, msg in failures:
            print(f"    - {api_id}: {url} -> 狀態碼: {code} ({msg}) (請人工確認是否因 WAF 或阻擋爬蟲導致)")
    else:
        print("[V] 所有文件連結存取正常！")

    return 0

if __name__ == "__main__":
    sys.exit(main())
