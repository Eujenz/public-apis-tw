# 台灣公共與開放 API 目錄收錄政策 (Catalog Policy)

本文件定義 `public-apis-tw` 專案之收錄標準、欄位規範、查核流程與退場退件機制。

---

## 1. 核心原則

1. **台灣關聯性 (Taiwan Relevance)**：以能輔助台灣開發者建構應用、服務在地使用者為優先考量。
2. **區分可程式化介面與靜態資料 (API vs Static Data)**：
   - 僅收錄具備 RESTful、GraphQL、SOAP、WebSocket、OGC Web Services (如 WMTS/WMS/WFS) 或其他可透過 HTTP/HTTPS 程式化即時調用之介面。
   - **嚴格排除純靜態資料下載**：政府資料開放平臺或其他網站上單純提供一次性 CSV、Excel、PDF、ODS 下載連結之資料集，不得視為 API 收錄。
   - 若靜態檔案或結構化數據是透過具有參數查詢、分頁或即時更新機制的正式 API 端點取得，則依其實際介面與使用方式判定收錄。
3. **客觀與真實性 (Truthfulness & Objectivity)**：
   - 欄位定義不容模糊：`last_reviewed_at` 代表人工查核中繼資料的日期；`last_endpoint_tested_at` 僅在實際對端點發送過 HTTP 請求且成功連線時填寫。
   - 未實際進行端點測試前，`verification_level` 不得標記為 `endpoint_tested`。
   - 未能確認的欄位以 `unknown` 標註，嚴禁憑空猜測或為求表格完整而捏造數值。

---

## 2. 分類原則 (Domain-Centric Categories)

目錄採用「主要使用領域」進行分類，而非以資料提供機關劃分（提供者屬性由 `provider_type` 表達）：

| 領域分類代碼 | 繁體中文名稱 | 收錄範圍說明 |
| :--- | :--- | :--- |
| **Government & Public Services** | 政府與公共服務 | 專門收錄跨部會整合資訊、一般公政、公用事業、各級政府大平台等不適合歸入特定垂直領域之服務。 |
| **Finance & Business** | 商業登記與金融財經 | 商工登記、上市櫃證券行情、期貨債券、電子發票、農產與大宗物資交易行情。 |
| **Weather & Environment** | 天氣與環境水情 | 氣象觀測預報、地震資訊與警報、空氣品質、水庫與河川水情、環境監測。 |
| **Transportation** | 交通與運輸 | 軌道運輸、公路客運、市區公車、公共自行車、道路路況與航空船舶。 |
| **Maps & Geospatial** | 地理資訊與國土測繪 | 電子地圖 WMTS/WMS、地籍地段圖層、門牌地址定位 (Geocoding) 與坐標轉換。 |
| **Culture & Tourism** | 文化與觀光 | 全國景點活動、藝文展演、合法旅宿與觀光休閒。 |
| **Healthcare & Public Health** | 醫療與公共衛生 | 健保特約院所時段、法定傳染病統計、公衛監測與醫療量能。 |
| **Education & Research** | 教育與學術研究 | 大專院校代碼、學術文獻期刊、研究機構典藏。 |
| **Developer Tools** | 開發者工具與輔助服務 | 台灣 3+3 郵遞區號剖析、中文地址正規化、在地化開發套件。 |
| **Other** | 其他開放服務 | 其他具備在地開發價值之特色介面。 |

---

## 3. 審查狀態 (`review_status`) 與服務狀態 (`service_status`)

本專案將「目錄中繼資料的審查進度」與「上游 API 本身的運作狀態」嚴格分離：

### 目錄審查狀態 (`review_status`)
- `candidate`：已提案或發現，但尚未完成官方文件與收錄條件核對。**不顯示於正式目錄主表**。
- `verified`：已完成來源、官方文件、驗證方式與收錄條件查核（注意：此標記表示中繼資料可信，不暗示端點長期保證可用）。
- `needs_review`：曾收錄但接獲回報端點改版、文件失效或規格變更，尚待維護者重新覆核。

### 服務可用狀態 (`service_status`)
- `active`：官方正常營運中之服務。
- `deprecated`：官方已公告即將棄用或已被新版取代。
- `unavailable`：端點長期處於中斷、關閉或無法連線狀態。
- `unknown`：上游營運狀態未知。

---

## 4. 技術查核等級 (`verification_level`) 與相容性規則

- `none`：未經查核（候選項目預設）。
- `docs_reviewed`：已人工核對官方技術文件、Swagger、參數規範與授權條款。
- `endpoint_tested`：已發出 HTTP 請求實際連線確認端點可達性（必須記錄 `last_endpoint_tested_at`）。
- `sample_response_checked`：已檢視實際回傳之 Payload 符合官方宣告 Schema。

**驗證相容性強制規則**：
1. 若 `review_status = verified`，則 `verification_level` 不得為 `none`（至少需為 `docs_reviewed`）。
2. 若 `verification_level = endpoint_tested` 或 `sample_response_checked`，則必須明確填寫 `last_endpoint_tested_at`，且 `review_status` 不得為 `candidate`。

---

## 5. 時效性與覆核過期機制 (Freshness & Expiry Policy)

API 規格與公部門服務常因機關組織改造、平台改版或政策變更而失效。本專案嚴格區分「歷史曾測試合格」與「近期確認有效」：

1. **中繼資料查核時效 (`last_reviewed_at`)**：
   - 有效評估期為 **365 天**。
   - 超過 365 天未重新人工核實者，CI 驗證工具將提出「查核已過期 (Freshness Warning)」提醒。
   - 超過 730 天（兩年）未曾覆核且無法自動取得存活訊號之條目，維護團隊應主動降級為 `review_status: needs_review`。
2. **端點實測時效 (`last_endpoint_tested_at`)**：
   - 實測標記僅代表發送請求當下之網路可達性與回應正確性。
   - `endpoint_tested` 記錄若超過 **90 天** 未執行新一輪 HTTP 健康檢查，目錄消費者應視為歷史證據，不得視為當下百分之百可用保證。
   - 專案將規劃定期端點存活健康監測腳本，持續更新實測時間戳記。

