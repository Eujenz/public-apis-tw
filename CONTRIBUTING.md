# Contributing to public-apis-tw (貢獻指南)

感謝您關注與支持 `public-apis-tw`！本專案的目標是為台灣開發者打造一份可靠、透明且維護良好的開放與公共 API 索引目錄。

我們歡迎任何符合標準的 API 提議、資訊勘誤與技術工具改進。

---

## 1. 收錄原則摘要

在提交新 API 之前，請務必詳閱 [收錄政策文件 (docs/catalog-policy.md)](docs/catalog-policy.md)。

收錄核心條件：
- **可程式化介面 (Programmable API)**：必須具備 RESTful、GraphQL、SOAP、WebSocket、OGC Web Services 等即時查詢端點。純靜態檔案（CSV、Excel、PDF）單純下載連結請勿提交。
- **領域分類原則**：依使用領域分類（例如氣象歸入 `Weather & Environment`，不因氣象署為公家機關而歸入政府類）。`Government & Public Services` 僅收錄不適合歸入其他特定垂直領域的一般公共服務。
- **具備公開技術文件**：必須附上官方或可信賴之 API Documentation 網址。
- **透明的驗證與費用**：清楚載明是否免金鑰或需 API Key，並標示免費額度。目前不收錄完全無免費額度之純商業付費服務。
- **客觀繁體中文**：以客觀中立之繁體中文描述，嚴禁宣傳或行銷用語。
- **誠實記錄查核狀態**：
  - `last_reviewed_at` 填寫您比對官方文件的日期。
  - 若未實際送出 HTTP 請求測試端點，請勿填寫 `last_endpoint_tested_at`，且 `verification_level` 請填 `docs_reviewed`。

---

## 2. 如何新增一筆 API

### 步驟 1：複製模板

從 `templates/api-template.yml` 複製一份檔案到 `data/apis/<id>.yml`：
- `<id>` 必須為唯一的 kebab-case 英文識別碼（例如 `moea-gcis-company.yml`）。
- 檔名 stem 必須與檔案內的 `id` 欄位完全相同。

### 步驟 2：填寫資料

請依 YAML 格式確實填寫各項欄位：
```yaml
id: "my-api-id"
name_zh: "範例 API"
name_en: "Example API"
description_zh: "提供台灣某項即時查詢之可程式化介面。"
category: "Government & Public Services" # 請使用定義好之 10 大領域分類之一
provider: "官方機構或社群組織"
provider_type: "official" # official 或 third_party
docs_url: "https://example.gov.tw/docs"
api_style: "REST" # REST, GraphQL, SOAP, WebSocket, OGC Web Services, OpenAPI, RPC, other, unknown
auth_type: "none" # none, api_key, oauth, other, unknown
access_tier: "free" # free, free_tier, paid, unknown
https_support: "yes" # yes, no, unknown
cors_support: "yes" # yes, no, unknown, not_applicable
license_name: "OGDL-Taiwan-1.0"
commercial_use: "allowed" # allowed, restricted, prohibited, unknown
service_status: "active" # active, deprecated, unavailable, unknown
review_status: "verified" # verified, candidate, needs_review
verification_level: "docs_reviewed" # docs_reviewed, endpoint_tested (僅限實測過者)
last_reviewed_at: "2026-10-13" # 查核當日 YYYY-MM-DD
sources:
  - "https://example.gov.tw/docs"
```

### 步驟 3：本地執行驗證與編譯

本專案使用標準現代化工具 [uv](https://docs.astral.sh/uv/)。請依序執行下列指令確認通過：

```bash
# 1. 同步虛擬環境與開發依賴
uv sync

# 2. 執行資料結構與規則驗證
uv run python scripts/validate_catalog.py

# 3. 執行單元與整合測試
uv run pytest

# 4. 編譯 Markdown 目錄與 JSON
uv run python scripts/build_catalog.py
```

### 步驟 4：送出 Pull Request

- 確保 `git status` 乾淨，已提交包含 `data/apis/<id>.yml`、`docs/catalog.md` 與 `dist/apis.json` 的更新。
- 送出 PR 時請勾選 PR 模板中的檢核項目。

---

## 3. 回報失效或資訊變更

若您在開發時發現本目錄收錄的 API 端點失效、文件連結 404 或規格已有重大調整：
- 請至 GitHub Issues 選擇「回報無效或變更的 API」表單。
- 或直接開 PR 修改對應之 YAML 檔案，更新狀態為 `needs_review`，由團隊進一步覆核。
