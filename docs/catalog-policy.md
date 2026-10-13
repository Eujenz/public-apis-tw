# 台灣公共與開放 API 目錄收錄政策 (Catalog Policy)

本文件定義 `public-apis-tw` 專案之收錄標準、欄位規範、查核流程與退場退件機制。

---

## 1. 核心原則

1. **台灣關聯性 (Taiwan Relevance)**：以能輔助台灣開發者建構應用、服務在地使用者為優先考量。
2. **具備可程式化介面 (Programmable API)**：
   - 僅收錄 RESTful、GraphQL、OpenAPI 或其他可透過 HTTP/HTTPS 程式化即時調用之介面。
   - 純靜態檔案（CSV、Excel、PDF、ODS 等下載連結）一律不列為 API 目錄。
3. **客觀與真實性 (Truthfulness & Objectivity)**：
   - 嚴格區分「已實測」與「僅查核文件」。未實際發起請求測試前，`verification_level` 不得標記為 `endpoint_tested`。
   - 未能確認的欄位以 `unknown` 標註，嚴禁憑空猜測或為求表格完整而捏造數值。

---

## 2. 欄位定義與規範

| 欄位 | 必要性 | 允許值 / 說明 |
| :--- | :--- | :--- |
| `id` | 必填 | 唯一識別代碼，小寫英文 kebab-case，必須與檔名相同。 |
| `name_zh` | 必填 | 繁體中文名稱。 |
| `name_en` | 選填 | 英文官方名稱。 |
| `description_zh` | 必填 | 客觀說明此 API 之功能用途與使用情境。 |
| `category` | 必填 | 必須為定義之 10 大類別之一。 |
| `provider` | 必填 | 提供機關、法人或開發團隊名稱。 |
| `provider_type` | 必填 | `official`（官方原創主管機關）或 `third_party`（第三方介接或社群服務）。 |
| `docs_url` | 必填 | 技術文件或 API 說明首頁。 |
| `base_url` | 選填 | API 基礎端點網址（不確定時省略）。 |
| `api_style` | 必填 | `REST`, `GraphQL`, `SOAP`, `OpenAPI`, `RPC`, `other`, `unknown`。 |
| `auth_type` | 必填 | `none`（完全公開免金鑰）, `api_key`, `oauth`, `other`, `unknown`。 |
| `access_tier` | 必填 | `free`（全免）, `free_tier`（有免費額度）, `paid`, `unknown`。第一版排除純付費且無免費試用之項目。 |
| `https_support` | 必填 | `yes`, `no`, `unknown`。 |
| `cors_support` | 必填 | `yes`, `no`, `unknown`, `not_applicable`。 |
| `license_name` | 必填 | 授權條款名稱，例如 `OGDL-Taiwan-1.0`、`CC BY 4.0`、`Proprietary`、`unknown`。 |
| `commercial_use` | 必填 | `allowed`（允許商用）, `restricted`（有限制）, `prohibited`（禁止）, `unknown`。 |
| `service_status` | 必填 | `active`, `deprecated`, `unavailable`, `unknown`。 |
| `review_status` | 必填 | `verified`（已完成文件來源審查）, `candidate`（候選待審）, `deprecated`（已棄用）。 |
| `verification_level`| 必填 | `none`, `docs_reviewed`, `endpoint_tested`, `sample_response_checked`。 |
| `last_verified_at` | 必填 | 最近查核日期 (YYYY-MM-DD)。 |
| `sources` | 必填 | 驗證此條目所引用的官方或第三方網址清單。 |

---

## 3. 審查狀態 (Review Status) 與查核等級 (Verification Level)

- **審查狀態 (`review_status`)**：
  - `candidate`：已提交但尚未經過維護團隊比對官方文件，不可進入 `docs/catalog.md` 正式主表。
  - `verified`：已比對官方來源確認真實存在，並符合本規範。
  - `deprecated`：已證實停止維護、端點關閉或不再支援。
- **查核等級 (`verification_level`)**：
  - `none`：未經查核。
  - `docs_reviewed`：已檢視官方技術文件，確認規格、驗證方式與授權條款。
  - `endpoint_tested`：已發出 HTTP 請求實際連線確認端點可達性。
  - `sample_response_checked`：已檢查回傳之 Payload 符合官方定義格式。

---

## 4. 排除與退件標準

下列項目不予收錄：
1. 僅提供一次性檔案下載、無即時查詢介面的開放資料集。
2. 無官方文件或由不明來源架設、無法確認資安與真實性之代理。
3. 商業付費服務但未提供任何免費方案/測試額度者。
4. 違反台灣法規或未獲資料所有人授權之爬蟲轉介 API。
