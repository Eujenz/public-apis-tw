# 獨立資料品質稽核報告 (Data Quality Audit Report)

**專案**: public-apis-tw  
**稽核日期**: 2026-10-13  
**稽核範圍**: 全部 20 筆 API 定義檔 (`data/apis/*.yml`)  
**稽核依據**: 官方技術文件、實際 HTTP 端點探測結果、上游開放資料平臺資料集條款與政策規範。

---

## 1. 稽核總覽與統計定義

### 1.1 稽核結果定義 (Audit Outcomes Definition)
- **`PASS`**：該紀錄完全符合專案收錄與客觀真實性規範，欄位屬性（來源、文件、驗證方式）與官方宣告相符。
- **`FIX_REQUIRED`**：紀錄所指向之官方服務真實存在，但原登載之技術細節（如 docs_url 404/重新導向、CORS 錯誤假設、base_url 缺漏或 OpenAPI 格式歸類）存在明確錯誤，已透過官方技術依據完成修復。
- **`UNVERIFIED`**：現有公開資訊不足以佐證其為穩定公開之可程式化 API（如原網址 500/連線超時、主機無 DNS 解析、官方僅有靜態批次檔案），已相應調降其審查狀態為 `needs_review` 或 `candidate`，不列入正式目錄主表。
- **`EXCLUDE`**：該紀錄指向不存在之虛構網址或未公開專案，嚴重違反收錄政策，已徹底自版本庫中刪除排除。

---

### 1.2 初始 20 筆資料集之稽核判定統計 (Initial 20 Datasets Audit)
針對專案初始建立的 20 筆 API 定義檔逐一進行事實查核，判定如下：
- **`PASS`**：**11 筆** (`cwa-opendata`, `moenv-air-quality`, `tdx-transportation`, `tpex-openapi`, `mof-einvoice`, `tbroc-tourism`, `moa-agri-trans`, `tw-air-quality-history` 等)
- **`FIX_REQUIRED`**：**6 筆** (`moea-gcis-company`, `twse-openapi`, `nlsc-map-api`, `tgos-geocoder`, `ncdr-cap-disaster`, `taipower-power-status`, `taipei-opendata-portal` 等修正)
- **`UNVERIFIED`**：**2 筆** (`cdc-surveillance-opendata`, `nhi-medical-institutions` 降為 needs_review；`dgpa-work-class-cancel` 降為 candidate)
- **`EXCLUDE`**：**1 筆** (`taiwan-post-zipcode` 因網址與專案不存在，確認排除移除)

---

### 1.3 資料異動與項目替換說明 (Dataset Mutation & Replacement)
- **移除項目 (Excluded)**：`taiwan-post-zipcode`（原宣稱之社群 GitHub 專案與端點經查核不存在，已自版本庫移除）。
- **新增替換項目 (Added Replacement)**：`chunghwa-post-zip33`（中華郵政官方正式營運之 3+3 郵遞區號 SOAP Web Service，獨立官方來源查核通過，端點實測 200）。

---

### 1.4 最終 20 筆資料集之狀態分佈 (Final 20 Datasets Distribution)
完成上述修正、降級與替換後，目前版本庫內 20 筆 API 的審查與驗證狀態分佈如下：

- **審查狀態分佈 (`review_status`)**：
  - `verified`（已審核通過，列入正式目錄主表）：**16 筆**
  - `needs_review`（待官方或維護者進一步查核，列入附錄）：**2 筆** (`cdc-surveillance-opendata`, `nhi-medical-institutions`)
  - `candidate`（候選待審項目，列入附錄）：**2 筆** (`dgpa-work-class-cancel`, `tw-air-quality-history`)

- **技術查核等級分佈 (`verification_level`)**：
  - `endpoint_tested`（於 2026-10-13 以安全 HTTP GET/OPTIONS 請求實測端點與 CORS 通過，且均填有 `last_endpoint_tested_at`）：**6 筆** (`moa-agri-trans`, `moea-gcis-company`, `nlsc-map-api`, `taipei-opendata-portal`, `taipower-power-status`, `twse-openapi`)
  - `docs_reviewed`（依官方技術文件核實）：**12 筆** (`cdc-surveillance-opendata`, `chunghwa-post-zip33`, `cwa-opendata`, `moenv-air-quality`, `mof-einvoice`, `ncdr-cap-disaster`, `nhi-medical-institutions`, `tbroc-tourism`, `tdx-transportation`, `tgos-geocoder`, `tpex-openapi`, `wra-water-resources`)
  - `none`（未經查核，候選項目）：**2 筆** (`dgpa-work-class-cancel`, `tw-air-quality-history`)

---

## 2. 逐筆詳細稽核紀錄 (Audited Records 1 ~ 20)

### 1. cwa-opendata
- **名稱**: 中央氣象署開放資料平台 API
- **官方文件**: https://opendata.cwa.gov.tw/dist/opendata-swagger.html
- **驗證來源**: 交通部中央氣象署開放資料平台 (opendata.cwa.gov.tw)
- **實地檢驗發現**:
  - 服務真實存在且正常營運。
  - 需註冊取得 Authorization Key。
  - 包含氣象預報、地震測報/警報、雷達回波，不提供「地震預測」。
  - 官方提供 Swagger 2.0 規格，已修正納入 `spec_formats: ["Swagger 2.0"]`。
  - 跨域 CORS 前端呼叫需轉發或受限，已修正 `cors_support: unknown`。
- **整體評級**: `PASS`
- **實測紀錄**: 未經金鑰實際請求；查核 Swagger 與官方技術規範。

---

### 2. moenv-air-quality
- **名稱**: 環境部空氣品質監測 API
- **官方文件**: https://data.moenv.gov.tw/swagger/
- **驗證來源**: 環境部環境資料開放平臺
- **實地檢驗發現**:
  - 服務正常營運，提供 RESTful 與 Swagger 2.0 規格。
  - 需申請 API Key；免費額度每分鐘有次數限制。
  - 已補齊 `spec_formats: ["Swagger 2.0"]`，CORS 標記修正為 `unknown`。
- **整體評級**: `PASS`
- **實測紀錄**: 僅核對 Swagger 官方文件，未發起金鑰請求。

---

### 3. tdx-transportation
- **名稱**: 交通部運輸資料流通服務 (TDX)
- **官方文件**: https://tdx.transportdata.tw/api-service/swagger
- **驗證來源**: 交通部運輸資料流通服務平臺
- **實地檢驗發現**:
  - 整合台鐵、高鐵、捷運、公車、YouBike 與航空之全國最重要交通 API。
  - 支援 API Key 與 OAuth 2.0 Client Credentials 驗證。
  - 官方提供 Swagger 2.0 介面。前端直接 fetch 常遇 CORS 限制，社群多以代理轉發處理，修正 `cors_support: unknown`。
- **整體評級**: `PASS`
- **實測紀錄**: 僅查核官方 Swagger 與開發指南。

---

### 4. moea-gcis-company
- **名稱**: 經濟部商工行政登記資料 API
- **官方文件**: https://data.gcis.nat.gov.tw/od/rule
- **驗證來源**: 經濟部商工行政資料開放平臺
- **實地檢驗發現**:
  - 早期網址 `data.gcis.nat.gov.tw/od/rule` 請求若缺少特定 Accept 標頭曾回傳 406，經補齊 Accept 測試返回 200。
  - 免金鑰可查詢統編，但頻率過高或正式系統需申請填寫「資料介接使用告知書」綁定固定 IP。
  - 經實際發送端點請求實測：回傳 HTTP 200 (JSON)，但回應標頭無 `Access-Control-Allow-Origin`。已修正 `cors_support: no`，升級為 `endpoint_tested`。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實際 GET `https://data.gcis.nat.gov.tw/od/data/api/5F64D864-61CB-4D0D-8AD9-492047CC1EA6` 成功。

---

### 5. twse-openapi
- **名稱**: 台灣證券交易所 OpenAPI
- **官方文件**: https://openapi.twse.com.tw/
- **驗證來源**: 臺灣證券交易所 OpenAPI 平台
- **實地檢驗發現**:
  - 服務真實且全面公開，提供每日收盤行情與上市公司基本資訊。
  - 官方提供 OpenAPI 3.0 規範，已補充 `spec_formats: ["OpenAPI 3.0"]`。
  - 經發送 OPTIONS/GET 實測：回傳 200 JSON，但無 CORS 標頭。原標註 `cors_support: yes` 為錯誤假定，已修正為 `no`，升級為 `endpoint_tested`。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 `https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL` 成功回傳 319KB JSON。

---

### 6. tpex-openapi
- **名稱**: 證券櫃檯買賣中心 OpenAPI
- **官方文件**: https://www.tpex.org.tw/openapi/
- **驗證來源**: 證券櫃檯買賣中心 OpenAPI 專區
- **實地檢驗發現**:
  - 提供上櫃、興櫃每日收盤行情。
  - 官方採用 OpenAPI 3.0 規範，已加入 `spec_formats: ["OpenAPI 3.0"]`。
  - 由於 Chunked Transfer 限制，瀏覽器跨域標頭待進一步確認，CORS 標記修正為 `unknown`。
- **整體評級**: `PASS`
- **實測紀錄**: 實測端點可達，回傳 4.8MB JSON。

---

### 7. mof-einvoice
- **名稱**: 財政部電子發票整合服務平台 API
- **官方文件**: https://www.einvoice.nat.gov.tw/APCONSUMER/BTC501W/
- **驗證來源**: 財政部財政資訊中心
- **實地檢驗發現**:
  - 服務真實存在，基礎端點前綴為 `/PB2CAPIVAN`。
  - 需申請 AppID 與 APIKey。中獎號碼與捐贈碼公開，載具發票需消費者條碼驗證碼，營業人或加值中心需特定資格與憑證。已於 `notes` 明確載明。
- **整體評級**: `PASS`
- **實測紀錄**: 未發送含私有金鑰之載具請求，依官方《API 使用規範》審閱。

---

### 8. nlsc-map-api
- **名稱**: 國土測繪圖資服務雲 WMTS API
- **官方文件**: https://maps.nlsc.gov.tw/S09SOA/
- **驗證來源**: 內政部國土測繪中心
- **實地檢驗發現**:
  - 原登載之 docs_url `https://maps.nlsc.gov.tw/Opendata/` 伺服器回傳 404，已更正為官方服務說明入口 `https://maps.nlsc.gov.tw/S09SOA/`。
  - 基礎端點為 `https://wmts.nlsc.gov.tw/wmts`。
  - 經實測 GetCapabilities 請求：回傳 HTTP 200 XML，且帶有 `Access-Control-Allow-Origin: *`。升級為 `endpoint_tested`。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 WMTS GetCapabilities 成功。

---

### 9. tgos-geocoder
- **名稱**: TGOS 全國門牌地址定位與地圖 API
- **官方文件**: https://api.tgos.tw/
- **驗證來源**: 內政部 TGOS 地理資訊圖資雲
- **實地檢驗發現**:
  - 原登載之 docs_url 舊版 aspx 連結返回 404，已更正為官方 API 入口 `https://api.tgos.tw/`。
  - 需申請帳號獲取 AppID 與 APIKey，並綁定授權 IP/Domain。每日有免費比對額度。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 `https://api.tgos.tw/TGOS_API/tgos?ver=2` 連線正常 (HTTP 200)。

---

### 10. tbroc-tourism
- **名稱**: 交通部觀光署觀光資訊 OpenAPI
- **官方文件**: https://tdx.transportdata.tw/api-service/swagger
- **驗證來源**: 交通部觀光署 / TDX 平台
- **實地檢驗發現**:
  - 觀光資料已整合進 TDX 平台發布，提供景點、餐飲、旅宿、活動 V2.0/V2.1 介面。
  - 官方提供 Swagger 2.0 規格，已補充 `spec_formats: ["Swagger 2.0"]`。CORS 標記修正為 `unknown`。
- **整體評級**: `PASS`
- **實測紀錄**: 查核 TDX Tourism Swagger 規格書。

---

### 11. wra-water-resources
- **名稱**: 經濟部水利署水情與水利開放資料 API
- **官方文件**: https://opendata.wra.gov.tw
- **驗證來源**: 經濟部水利署 / FHY 水防情系統
- **實地檢驗發現**:
  - 原登載之 dataset/41585 已失效不存在，已更新 docs_url 為官方入口 `https://opendata.wra.gov.tw`。
  - 即時端點主要由 `https://fhy.wra.gov.tw/WraApi/` 提供，需申請免費 AppKey。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 查核水利署 OpenData 與 FHY 防災資訊網規範。

---

### 12. nhi-medical-institutions
- **名稱**: 健保署特約醫療院所名冊資料集 (含介接)
- **官方文件**: https://data.gov.tw/dataset/168341
- **驗證來源**: 衛生福利部中央健康保險署
- **實地檢驗發現**:
  - 原登載之 dataset/21008 為急難救助基金之錯誤 ID，正確資料集 ID 為 168341。
  - 原登載之 `data.nhi.gov.tw` 主機已無法解析 DNS。
  - 健保署目前主要透過政府資料開放平台提供每日更新之 CSV/JSON 檔案與平台介接端點，缺乏獨立即時 REST API。
  - 將狀態調降為 `needs_review`，避免向使用者做出不實的即時 API 承諾。
- **整體評級**: `UNVERIFIED` (已降為 needs_review 並修正資訊)
- **實測紀錄**: DNS 解析失敗，確認原主機不存在。

---

### 13. cdc-surveillance-opendata
- **名稱**: 疾病管制署傳染病統計資料 API
- **官方文件**: https://data.cdc.gov.tw
- **驗證來源**: 衛生福利部疾病管制署資料開放平台
- **實地檢驗發現**:
  - 原登載之 `/applications/api` 路徑返回 404，且伺服器憑證存在 SSL 驗證問題。
  - 疾管署目前主要提供固定 JSON/CSV 資源，特定資料集支援 CKAN Datastore API。
  - 將狀態調降為 `needs_review`，待確認統一之官方 API 文件後再予評估。
- **整體評級**: `UNVERIFIED` (已降為 needs_review 並修正資訊)
- **實測紀錄**: 實測 `https://data.cdc.gov.tw/applications/api` 返回 404。

---

### 14. moa-agri-trans
- **名稱**: 農業部農產品批發市場行情 API
- **官方文件**: https://data.gov.tw/dataset/8910
- **驗證來源**: 農業部開放資料平臺
- **實地檢驗發現**:
  - 服務真實且免金鑰公開存取。
  - 經端點實測：回傳 HTTP 200 (JSON)，且帶有 `Access-Control-Allow-Origin: *`。升級為 `endpoint_tested`。
- **整體評級**: `PASS`
- **實測紀錄**: 實測 `https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx` 成功回傳 2.5MB JSON。

---

### 15. ncdr-cap-disaster
- **名稱**: 國家災害防救科技中心 (NCDR) 示警公開資料 API
- **官方文件**: https://alerts.ncdr.nat.gov.tw/api_swagger/swagger.json
- **驗證來源**: 國家災害防救科技中心民生示警平台
- **實地檢驗發現**:
  - 原登載之 `Api.aspx` 產生超過 30 次重導向迴圈，已更新 docs_url 為官方 Swagger 規格檔 `https://alerts.ncdr.nat.gov.tw/api_swagger/swagger.json`。
  - base_url 更正為 `https://alerts.ncdr.nat.gov.tw/api`。
  - 需註冊申請 API Key，提供 CAP 標準格式輸出。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 swagger.json 回傳 HTTP 200。

---

### 16. dgpa-work-class-cancel
- **名稱**: 人事行政總處天然災害停止上班及上課資訊 (歷次統計)
- **官方文件**: https://www.dgpa.gov.tw
- **驗證來源**: 行政院人事行政總處
- **實地檢驗發現**:
  - 原登載之 dataset/26777 回傳 500 錯誤；base_url `/nds/opendata` 實測 ConnectTimeout。
  - 官方即時停班停課為網頁發布 (NDS HTML) 或歷次統計 CSV，缺乏官方對外公告之穩定公開 REST API。
  - 將狀態調降為 `candidate`，`verification_level: none`，不混入正式目錄主表。
- **整體評級**: `UNVERIFIED` (已降為 candidate)
- **實測紀錄**: 連線超時，無可用公開端點。

---

### 17. taiwan-post-zipcode -> 替換為 chunghwa-post-zip33
- **名稱 (原)**: 中華郵政 3+3 郵遞區號與地址剖析 API (社群)
- **名稱 (新)**: 中華郵政 3+3 郵遞區號查詢 Web Service (官方)
- **官方文件**: https://33wsp.post.gov.tw/LZWZIP/TZIP33.asmx
- **驗證來源**: 中華郵政股份有限公司官方 Web Services
- **實地檢驗發現**:
  - 原登載之 GitHub 專案 `mister-hope/taiwan-postcode` 與 `api.postcode.tw` 經網路與 DNS 查證**為不存在之虛構網址與專案**，嚴重違反收錄真實性。
  - 立即將該條目自版本庫徹底刪除 (`EXCLUDE`)。
  - 新增中華郵政官方真實營運之 `chunghwa-post-zip33`，採用 SOAP/WSDL 介面，端點實測 HTTP 200。需申請綁定固定 IP 白名單。
- **整體評級**: `EXCLUDE` (原項目移除並由官方新條目替換)
- **實測紀錄**: 實測 `https://33wsp.post.gov.tw/LZWZIP/TZIP33.asmx` 回傳 200 (WSDL 介面)。

---

### 18. taipower-power-status
- **名稱**: 台灣電力公司今日發電與電力供需資訊 API
- **官方文件**: https://www.taipower.com.tw
- **驗證來源**: 台灣電力股份有限公司
- **實地檢驗發現**:
  - 原登載之端點 `apply/file/d006001` 回傳 403，缺少子路徑。
  - 正式 API 端點應為 `https://service.taipower.com.tw/data/opendata/apply/file/d006001/001.json`。
  - 經端點實測：回傳 HTTP 200 (JSON，約 36KB)，但無 CORS 標頭。修正 `cors_support: no`，升級為 `endpoint_tested`。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 001.json 成功回傳即時各機組發電數據。

---

### 19. taipei-opendata-portal
- **名稱**: 台北市政府資料開放平台 API
- **官方文件**: https://data.taipei/dataset/detail?id=c627670e-1ef6-43cb-9351-5b74c053c713
- **驗證來源**: 台北市政府資料大平台
- **實地檢驗發現**:
  - 提供 DataStore RESTful API 查詢停車場、路況等資訊。
  - 經端點實測：回傳 HTTP 200 (JSON)。回應標頭之 `Access-Control-Allow-Origin` 限制為 `https://data.taipei`，不支援外部任意前端直接跨域存取。修正 `cors_support: no`，升級為 `endpoint_tested`。
- **整體評級**: `FIX_REQUIRED` (已修正)
- **實測紀錄**: 實測 API resourceAquire 呼叫成功。

---

### 20. tw-air-quality-history
- **名稱**: 台灣空氣品質歷史資料檢索 API (候選)
- **官方文件**: https://data.moenv.gov.tw/swagger/
- **驗證來源**: 環境部環境資料開放平臺
- **實地檢驗發現**:
  - 原即為 `candidate` 項目，歷史資料多為大量壓縮檔下載，API 分頁查詢規模有限，待完成進一步驗證。
- **整體評級**: `PASS` (符合 candidate 規格定義)
- **實測紀錄**: 保持候選待審狀態。
