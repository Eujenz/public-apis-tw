# 台灣公共與開放 API 目錄 (Public APIs Taiwan Catalog)

> 本文件由原始資料自動產生，請勿手動直接編輯。如需修正請修改 `data/apis/*.yml` 並執行 `uv run python scripts/build_catalog.py`。

## 摘要統計

- **正式收錄 (Verified)**: 16 項
- **候選項目 (Candidate)**: 2 項
- **待重新覆核 (Needs Review)**: 2 項
- **最後編譯時間**: 自動更新於每次建置

## 分類快速導覽

- [政府與公共服務 (Government & Public Services)](#government-public-services) (4)
- [商業登記與金融財經 (Finance & Business)](#finance-business) (5)
- [天氣與環境水情 (Weather & Environment)](#weather-environment) (3)
- [交通與運輸 (Transportation)](#transportation) (1)
- [地理資訊與國土測繪 (Maps & Geospatial)](#maps-geospatial) (2)
- [文化與觀光 (Culture & Tourism)](#culture-tourism) (1)
- [教育與學術研究 (Education & Research)](#education-research) (0)
- [醫療與公共衛生 (Healthcare & Public Health)](#healthcare-public-health) (0)
- [開發者工具與輔助服務 (Developer Tools)](#developer-tools) (0)
- [其他開放服務 (Other)](#other) (0)

---

## 政府與公共服務 (Government & Public Services)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **中華郵政 3+3 郵遞區號查詢 Web Service**<br>`Chunghwa Post 3+3 Postal Code Query Web Service` | 中華郵政股份有限公司 | 提供台灣標準地址正規化與 3+3 郵遞區號查詢、縣市行政區反查之官方 SOAP Web Service 介面。 | `SOAP` | `other` | `free` | `yes` | `not_applicable` | `OGDL-Taiwan-1.0` | [文件連結](https://33wsp.post.gov.tw/LZWZIP/TZIP33.asmx) | `docs_reviewed` |
| **國家災害防救科技中心 (NCDR) 示警公開資料 API**<br>`NCDR Common Alerting Protocol (CAP) Disaster Warning API` | 國家災害防救科技中心 (NCDR) | 彙整中央氣象署、水利署、農村水保署、公路局等跨部會之天然災害（颱風、豪雨、土石流、地震）標準 CAP 示警訊號。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://alerts.ncdr.nat.gov.tw/api_swagger/swagger.json) | `docs_reviewed` |
| **台北市政府資料開放平台 API**<br>`Taipei City OpenData DataStore API` | 台北市政府資訊局 | 台北市政府資料大平台提供之資料集查詢、即時路況、停車場即時剩餘車位等 RESTful 介面。 | `REST` | `none` | `free` | `yes` | `no` | `OGDL-Taiwan-1.0` | [文件連結](https://data.taipei/dataset/detail?id=c627670e-1ef6-43cb-9351-5b74c053c713) | `endpoint_tested` |
| **台灣電力公司今日發電與電力供需資訊 API**<br>`Taipower Real-Time Electricity Generation & Supply API` | 台灣電力公司 | 提供台灣全島即時各機組發電量、能源類型佔比、當日用電曲線及供電備轉容量率。 | `REST` | `none` | `free` | `yes` | `no` | `OGDL-Taiwan-1.0` | [文件連結](https://www.taipower.com.tw) | `endpoint_tested` |

## 商業登記與金融財經 (Finance & Business)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **農業部農產品批發市場行情 API**<br>`MOA Agricultural Products Wholesale Market Price API` | 農業部 | 提供全台各果菜、花卉與肉品批發市場之每日各項農產品交易量、平均價與歷史價格查詢。 | `REST` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gov.tw/dataset/8910) | `endpoint_tested` |
| **經濟部商工行政登記資料 API**<br>`MOEA Commercial & Business Registration Open Data API` | 經濟部商業發展署 | 提供全國公司設立登記、商業登記、分公司資料及營業項目代碼之即時查詢介面。 | `REST` | `none` | `free` | `yes` | `no` | `OGDL-Taiwan-1.0` | [文件連結](https://data.gcis.nat.gov.tw/od/rule) | `endpoint_tested` |
| **財政部電子發票整合服務平台 API**<br>`MOF E-Invoice Open API` | 財政部財政資訊中心 | 提供電子發票中獎號碼開獎結果、載具發票表頭/明細查詢、營業人統編字軌有效性及捐贈碼查驗。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://www.einvoice.nat.gov.tw/APCONSUMER/BTC501W/) | `docs_reviewed` |
| **證券櫃檯買賣中心 OpenAPI**<br>`Taipei Exchange (TPEx) OpenAPI` | 證券櫃檯買賣中心 (TPEx) | 提供上櫃股票行情、興櫃股票交易資訊、公債市場與外幣計價債券每日統計之 OpenAPI 介面。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://www.tpex.org.tw/openapi/) | `docs_reviewed` |
| **台灣證券交易所 OpenAPI**<br>`Taiwan Stock Exchange (TWSE) OpenAPI` | 臺灣證券交易所 (TWSE) | 提供集中交易市場每日收盤行情、個股本益比/殖利率、除權息公告、大盤指數與上市基本資訊之 OpenAPI 介面。 | `REST` | `none` | `free` | `yes` | `no` | `OGDL-Taiwan-1.0` | [文件連結](https://openapi.twse.com.tw/) | `endpoint_tested` |

## 天氣與環境水情 (Weather & Environment)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **中央氣象署開放資料平台 API**<br>`CWA OpenData API` | 交通部中央氣象署 | 提供台灣氣象預報、即時天氣觀測、地震資訊與警報、氣象雷達及颱風警報資料之 RESTful 介面。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dist/opendata-swagger.html) | `docs_reviewed` |
| **環境部空氣品質監測 API**<br>`MOENV Air Quality API` | 環境部 | 提供全台各地測站即時空氣品質指標 (AQI)、PM2.5、PM10、臭氧及詳細大氣濃度數據。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/) | `docs_reviewed` |
| **經濟部水利署水情與水利開放資料 API**<br>`WRA Water Resources Open Data & FHY API` | 經濟部水利署 | 提供水庫蓄水量、水情燈號、全台河川水位、淹水感測警戒與雨量站觀測數據。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.wra.gov.tw) | `docs_reviewed` |

## 交通與運輸 (Transportation)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **交通部運輸資料流通服務 (TDX)**<br>`Transport Data eXchange (TDX)` | 交通部 | 整合台灣軌道 (台鐵/高鐵/捷運)、公路客運、市區公車、公共自行車 (YouBike) 與航空船舶之全國即時動態與靜態路網資料。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger) | `docs_reviewed` |

## 地理資訊與國土測繪 (Maps & Geospatial)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **國土測繪圖資服務雲 WMTS API**<br>`NLSC Web Map Tile Service (WMTS) API` | 內政部國土測繪中心 | 提供台灣全島通用版電子地圖、正射影像圖、國土利用現況圖及村里行政界線等 OGC WMTS 圖磚服務。 | `OGC Web Services` | `none` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://maps.nlsc.gov.tw/S09SOA/) | `endpoint_tested` |
| **TGOS 全國門牌地址定位與地圖 API**<br>`TGOS Address Geocoding & Map API` | 內政部資訊服務司 / 國土測繪圖資雲 | 內政部地理資訊圖資雲服務平台提供之門牌地址定位 (Geocoding)、坐標反查與地圖前端元件服務。 | `REST` | `api_key` | `free_tier` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://api.tgos.tw/) | `docs_reviewed` |

## 文化與觀光 (Culture & Tourism)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **交通部觀光署觀光資訊 OpenAPI**<br>`Taiwan Tourism Administration OpenData API` | 交通部觀光署 | 提供台灣全島景點、觀光活動、合法旅宿、在地餐飲與自行車道之即時活動與點位資料。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger) | `docs_reviewed` |

## 教育與學術研究 (Education & Research)

*目前此分類尚無已審核通過之項目。*

## 醫療與公共衛生 (Healthcare & Public Health)

*目前此分類尚無已審核通過之項目。*

## 開發者工具與輔助服務 (Developer Tools)

*目前此分類尚無已審核通過之項目。*

## 其他開放服務 (Other)

*目前此分類尚無已審核通過之項目。*
