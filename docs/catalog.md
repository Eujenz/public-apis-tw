# 台灣公共與開放 API 目錄 (Public APIs Taiwan Catalog)

> 本文件由原始資料自動產生，請勿手動直接編輯。如需修正請修改 `data/apis/*.yml` 並執行 `uv run python scripts/build_catalog.py`。

## 摘要統計

- **正式收錄 (Verified)**: 19 項
- **候選項目 (Candidate)**: 1 項
- **最後編譯時間**: 自動更新於每次建置

## 分類快速導覽

- [政府與公共服務 (Government & Public Services)](#government-public-services) (4)
- [商業登記與金融財經 (Finance & Business)](#finance-business) (5)
- [天氣與環境水情 (Weather & Environment)](#weather-environment) (3)
- [交通與運輸 (Transportation)](#transportation) (1)
- [地理資訊與國土測繪 (Maps & Geospatial)](#maps-geospatial) (2)
- [文化與觀光 (Culture & Tourism)](#culture-tourism) (1)
- [教育與學術研究 (Education & Research)](#education-research) (0)
- [醫療與公共衛生 (Healthcare & Public Health)](#healthcare-public-health) (2)
- [開發者工具與輔助服務 (Developer Tools)](#developer-tools) (1)
- [其他開放服務 (Other)](#other) (0)

---

## 政府與公共服務 (Government & Public Services)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **人事行政總處天然災害停止上班及上課 API**<br>`DGPA Disaster Work & School Cancellation API` | 行政院人事行政總處 (DGPA) | 提供天然災害（颱風、豪雨、地震）發生時，台灣各縣市通報之停止上班上課（停班停課）即時狀態公告。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/26777) | `docs_reviewed` |
| **國家災害防救科技中心 (NCDR) 示警公開資料 API**<br>`NCDR Common Alerting Protocol (CAP) Disaster Warning API` | 國家災害防救科技中心 (NCDR) | 彙整台灣中央氣象署、水利署、水保署、公路局等跨部會之即時天然災害（颱風、豪雨、土石流、地震、道路阻斷）標準 CAP 示警訊號。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://alerts.ncdr.nat.gov.tw/Api.aspx) | `docs_reviewed` |
| **台北市政府資料開放平台 API**<br>`Taipei City OpenData DataStore API` | 台北市政府資訊局 | 台北市政府資料大平台提供之 CKAN-like 資料集查詢、即時路況、停車場即時剩餘車位等 RESTful 介面。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.taipei/dataset/detail?id=c627670e-1ef6-43cb-9351-5b74c053c713) | `docs_reviewed` |
| **台灣電力公司今日供電資訊 API**<br>`Taiwan Power Company Electricity Supply Status API` | 台灣電力公司 | 提供台灣全島當日用電曲線、預估最高用電量、即時淨發購電量及備轉容量率燈號。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/19995) | `docs_reviewed` |

## 商業登記與金融財經 (Finance & Business)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **農業部農產品批發市場行情 API**<br>`MOA Agricultural Products Wholesale Market Price API` | 農業部 | 提供全台各果菜、花卉與肉品批發市場之每日各項農產品交易量、平均價與歷史價格查詢。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/8910) | `docs_reviewed` |
| **經濟部商工登記資料 API**<br>`MOEA Business Registration OpenData API` | 經濟部商業發展署 | 提供台灣全國公司設立登記、商業登記、分公司資料及營業項目代碼之即時查詢介面。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gcis.nat.gov.tw/od/rule) | `docs_reviewed` |
| **財政部電子發票整合服務平台 API**<br>`MOF E-Invoice Open API` | 財政部財政資訊中心 | 提供電子發票中獎號碼開獎結果、載具發票表頭/明細查詢、營業人統編字軌有效性及捐贈碼查驗。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://www.einvoice.nat.gov.tw/APCONSUMER/BTC501W/) | `docs_reviewed` |
| **證券櫃檯買賣中心 OpenAPI**<br>`Taipei Exchange (TPEx) OpenAPI` | 證券櫃檯買賣中心 (TPEx) | 提供台灣上櫃股票行情、興櫃股票交易資訊、公債市場與外幣計價債券每日統計之 OpenAPI 介面。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://www.tpex.org.tw/openapi/) | `docs_reviewed` |
| **台灣證券交易所 OpenAPI**<br>`Taiwan Stock Exchange (TWSE) OpenAPI` | 臺灣證券交易所 (TWSE) | 提供台灣集中交易市場每日收盤行情、個股本益比/殖利率、除權息公告、大盤指數與上市基本資訊之 OpenAPI 介面。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://openapi.twse.com.tw/) | `docs_reviewed` |

## 天氣與環境水情 (Weather & Environment)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **中央氣象署開放資料平台 API**<br>`CWA OpenData API` | 交通部中央氣象署 | 提供台灣氣象預報、即時天氣觀測、地震資訊與警報、氣象雷達及颱風警報資料之 RESTful 介面。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dist/opendata-swagger.html) | `docs_reviewed` |
| **環境部空氣品質監測 API**<br>`MOENV Air Quality API` | 環境部 | 提供全台各地測站即時空氣品質指標 (AQI)、PM2.5、PM10、臭氧及詳細大氣濃度數據。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/) | `docs_reviewed` |
| **經濟部水利署水資源即時資料 API**<br>`WRA Real-time Water Resources API` | 經濟部水利署 | 提供台灣主要水庫蓄水量、水情燈號、全台河川水位、淹水警戒與雨量站觀測數據。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/41585) | `docs_reviewed` |

## 交通與運輸 (Transportation)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **交通部運輸資料流通服務 (TDX)**<br>`Transport Data eXchange (TDX)` | 交通部 | 整合台灣軌道 (台鐵/高鐵/捷運)、公路客運、市區公車、公共自行車 (YouBike) 與航空船舶之全國即時動態與靜態路網資料。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger) | `docs_reviewed` |

## 地理資訊與國土測繪 (Maps & Geospatial)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **國土測繪圖資服務雲 API**<br>`NLSC Web Map & Coordinate API` | 內政部國土測繪中心 | 提供台灣全島通用版電子地圖 (WMTS)、正射影像圖、地段代碼查詢、地籍圖層與坐標轉換服務。 | `OGC Web Services` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://maps.nlsc.gov.tw/Opendata/) | `docs_reviewed` |
| **TGOS 全國地理資訊圖資雲門牌地址定位 API**<br>`TGOS Address Geocoding API` | 內政部地政司 / 資訊中心 | 內政部地理資訊圖資雲服務平台提供之標準門牌地址定位 (Geocoding) 與坐標反查服務。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://www.tgos.tw/TGOS/Web/Services/TGOS_Services.aspx) | `docs_reviewed` |

## 文化與觀光 (Culture & Tourism)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **交通部觀光署觀光資訊 OpenAPI**<br>`Taiwan Tourism Administration OpenData API` | 交通部觀光署 | 提供台灣全島景點、觀光活動、合法旅宿、在地餐飲與自行車道之即時活動與點位資料。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger) | `docs_reviewed` |

## 教育與學術研究 (Education & Research)

*目前此分類尚無已審核通過之項目。*

## 醫療與公共衛生 (Healthcare & Public Health)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **疾病管制署傳染病統計資料 API**<br>`Taiwan CDC Infectious Disease Surveillance API` | 衛生福利部疾病管制署 | 提供台灣法定傳染病（登革熱、流感、腸病毒、COVID-19 等）依縣市鄉鎮、年齡別與週別之確定病例數統計查詢。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.cdc.gov.tw/applications/api) | `docs_reviewed` |
| **健保署特約醫療院所與即時服務 API**<br>`NHI Contracted Medical Facilities API` | 衛生福利部中央健康保險署 | 提供台灣全台健保特約醫院、診所、特約藥局基本資料、診療科別與就醫服務時段查詢。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/21008) | `docs_reviewed` |

## 開發者工具與輔助服務 (Developer Tools)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **中華郵政 3+3 郵遞區號與地址剖析 API (社群)**<br>`Taiwan Zipcode & Address Parser API (Community)` | g0v / 開源社群協作者 | 開源社群封裝之中華郵政新版 3+3 郵遞區號查詢與中文地址正規化斷詞 REST API。 | `REST` | `none` | `free` | `yes` | `yes` | `MIT` | [文件連結](https://github.com/mister-hope/taiwan-postcode) | `docs_reviewed` |

## 其他開放服務 (Other)

*目前此分類尚無已審核通過之項目。*
