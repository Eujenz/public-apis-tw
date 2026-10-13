---
name: api-doc-scraper
description: >-
  Scrapes modern JavaScript/SPA API documentation portals (e.g. Swagger UI, Redoc, TDX, CWA, e-Invoice)
  using Crawlee for Python and Playwright. Captures OpenAPI/Swagger JSON specifications via network
  interception, extracts API metadata, and produces schema-validated YAML entries for public-apis-tw.
---

# API Documentation Scraper (Crawlee + Playwright)

本 Skill 提供標準作業程序 (SOP)，指導 Agent 使用基於 [Crawlee for Python](https://github.com/apify/crawlee-python) 的爬蟲工具探索並採集台灣公共與開放 API 官方文件。

---

## 📌 觸發條件 (Trigger Conditions)

當使用者提出下列需求時，應激活並遵循此 Skill：
- 「請爬取/抓取某個 API 的官方文件（例如 TDX、氣象署、商工登記、電子發票等）」
- 「幫我分析某個 Swagger UI 或 SPA 網站的 API 規格並產出 YAML」
- 「自動探測並新增 API 到目錄」
- 需從複雜的 JavaScript 單頁式應用 (SPA) 提取底層 OpenAPI / Swagger 規格時

---

## ⚙️ 執行環境先決條件 (Prerequisites)

在首次執行爬蟲前，需確認已安裝選用的 `scraper` 依賴群組與 Chromium 瀏覽器核心：

```powershell
# 1. 安裝 scraper 依賴庫
uv sync --group scraper

# 2. 安裝 Playwright 瀏覽器二進位檔 (僅首次需要)
uv run --group scraper playwright install chromium
```

---

## 🚀 標準作業程序 (Standard Operating Procedure)

### 步驟 1：執行 Crawlee 爬蟲探測端點

使用專案內建的 `scripts/scrape_api_docs.py`，啟動無頭瀏覽器載入頁面，自動監聽網路封包並擷取 `openapi.json` / `swagger.json`：

```powershell
uv run --group scraper python scripts/scrape_api_docs.py `
  --url "https://tdx.transportdata.tw/api-service/swagger" `
  --api-id "tdx-transportation" `
  --output-yaml "data/apis/tdx-transportation.yml" `
  --output-json "data/raw_specs/tdx-swagger.json"
```

### 步驟 2：人工檢核與中繼資料補全

爬蟲產生的 YAML 條目預設為 `candidate` 狀態。檢視生成的 `data/apis/<id>.yml` 並依據真實文件補全：
1. **`category`**：對照目錄十大領域（例如 `Transportation`、`Weather & Environment` 等）。
2. **`name_zh` / `description_zh`**：確保為清晰客觀的繁體中文說明。
3. **`auth_type`**：確認為 `none`、`api_key`、`oauth` 還是其他形式。
4. **`license_name` / `license_url`**：政府單位多為 `OGDL-Taiwan-1.0`（網址：`https://data.gov.tw/license`）。
5. **`provider`**：填寫主管部會或提供單位（例如 `交通部`、`經濟部`）。

### 步驟 3：執行目錄驗證

確保編輯後的 YAML 符合 [`schemas/api.schema.json`](file:///c:/Users/LeeWei/Documents/public-apis-tw/schemas/api.schema.json)：

```powershell
uv run python scripts/validate_catalog.py
```

### 步驟 4：重新編譯正式目錄

通過驗證後，更新 Markdown 目錄與全量 JSON 檔案：

```powershell
uv run python scripts/build_catalog.py
uv run pytest
```

---

## 🛡️ 常見問題與例外處理 (Troubleshooting)

- **遇到 WAF / Cloudflare / 403 阻擋**：
  若無頭模式遭封鎖，可加上 `--no-headless` 進行可見視窗探測，或使用 `requests` 檢查是否有開放的靜態 Swagger JSON 直連網址。
- **未捕獲到 OpenAPI JSON**：
  若頁面非 Swagger UI，腳本會優雅退回提取 DOM Meta 與標題結構。此時應依據提取出的頁面資訊手動輔助確認端點路徑。
