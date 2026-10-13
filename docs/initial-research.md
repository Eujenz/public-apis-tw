# Initial Research & Landscape Analysis: public-apis-tw

## 1. 調查對象與專案背景

本研究盤點現有相關開源專案、政府資料平台與民間專案，以確立 `public-apis-tw` 的定位與收錄邊界：

1. **[public-apis/public-apis](https://github.com/public-apis/public-apis)**
   - **目標定位**：全球最大的集合性免費 API 清單（社群驅動的 Markdown 表格）。
   - **優點**：知名度高、格式清晰（API、Description、Auth、HTTPS、CORS）。
   - **缺點與限制**：對台灣在地服務收錄極少；未針對台灣官方政策、授權模式（如政府資料開放授權條款 OGDL-Taiwan）或繁體中文文件做深度標記；許多項目年久失修。

2. **[OpenFun (openfun.tw) / data.openfun.tw](https://openfun.tw/)**
   - **目標定位**：台灣民間開源團隊推動之公共資料鏡像與資料庫代理服務。
   - **優點**：提供整理過的台灣政府公開資料端點與介面，改善部分政府系統不易查詢的問題。
   - **差異與邊界**：OpenFun 屬於資料託管與代理實作；`public-apis-tw` 是純索引目錄，不架設後端代理、不重新託管資料庫，專注於索引「原創 API 與官方/可靠第三方端點」。

3. **[政府資料開放平台 (data.gov.tw)](https://data.gov.tw/)**
   - **目標定位**：中華民國政府官方資料開放單一入口。
   - **優點**：資料量龐大，涵蓋中央與地方各機關。
   - **差異與限制**：許多資源為純 CSV/XML/JSON 靜態檔案下載或網頁連結，而非標準 RESTful / 即時 API；開發者往往不易一眼判斷「哪些是具有 API 規格、即時查詢介面的服務」以及其驗證金鑰規範。

4. **[OpenData-TW/data.gov.tw](https://github.com/OpenData-TW/data.gov.tw)**
   - **目標定位**：社群維護之 data.gov.tw 資料集 metadata 快照與歷史變更追蹤。
   - **差異**：該專案著重於 platform metadata 備份；`public-apis-tw` 著重於可程式介接的 API 開發者指南與目錄。

5. **[api-evangelist/open-government-taiwan](https://github.com/api-evangelist/open-government-taiwan)**
   - **目標定位**：Kin Lane (API Evangelist) 早期整理的台灣政府開放 API 清單。
   - **差異**：早期概念驗證專案，收錄數量少且多年未更新，多數端點與文件連結已過時失效。

---

## 2. public-apis-tw 的差異化價值與定位

- **台灣開發者優先（Taiwan Developer First）**：以繁體中文撰寫客觀說明與使用規範，保留原生官方技術術語。
- **嚴格區分純檔案與 API**：僅收錄具備可程式化查詢介面（RESTful、GraphQL 等）之服務，排除純靜態 CSV/Excel/PDF 下載點。
- **結構化中繼資料**：透過嚴格的 JSON Schema 檢驗（YAML 原始檔 + JSON 產生檔），包含身份驗證方式、計費方案、CORS 支援、授權條款與測試驗證狀態。
- **明確標示驗證狀態（Review & Verification Levels）**：
  - `review_status`: `verified`（已完成文件核對）、`candidate`（候選）、`deprecated`（已棄用）。
  - `verification_level`: `docs_reviewed`（文件已核實）、`endpoint_tested`（實際發送過請求驗證）、`sample_response_checked`（回傳資料已檢驗）。未實際測試者絕不虛構填寫。

---

## 3. 初步資料來源與涵蓋範圍

第一版重點收錄涵蓋下列領域之可靠官方/關鍵第三方服務：
- **中央氣象署開放資料平台 (CWA OpenData)**
- **環境部空氣品質監測 API (MOENV)**
- **交通部 TDX (運輸資料流通服務)**
- **經濟部商業司商工登記資料 API**
- **內政部國土測繪圖資服務 (NLSC)**
- **財政部電子發票整合服務平台 API**
- **健保署/疾管署公開疫情與醫療院所資訊**
- **台灣證券交易所 (TWSE) / 櫃檯買賣中心 (TPEx) OpenAPI**
- **行政院農委會/農業部農業開放資料**
- **台灣郵遞區號/地址轉換服務 (如可靠之第三方/官方 API)**

---

## 4. 已知限制與後續原則

1. **不可盲目發起大規模端點爬取**：避免觸發政府或民間機關的 WAF / Rate Limiter。
2. **謹慎處理 API Key**：多數台灣官方 API（如 TDX、CWA、MOENV）皆需免費註冊取得金鑰。本專案不儲存或共享私有金鑰，僅標註申請流程與網址。
3. **授權條款嚴謹考證**：多數政府 API 遵循「政府資料開放授權條款 (OGDL-Taiwan-1.0)」，部分第三方則遵循 MIT、CC 或專屬商業條款，若未載明統一標記為 `unknown`。
