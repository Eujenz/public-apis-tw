# 台灣公共與開放 API 目錄 (Public APIs Taiwan Catalog)

> 本文件由原始資料自動產生，請勿手動直接編輯。如需修正請修改 `data/apis/*.yml` 並執行 `uv run python scripts/build_catalog.py`。

## 摘要統計

- **正式收錄 (Verified)**: 41 項
- **候選項目 (Candidate)**: 16 項
- **待重新覆核 (Needs Review)**: 2 項
- **最後編譯時間**: 自動更新於每次建置

## 分類快速導覽

- [政府與公共服務 (Government & Public Services)](#government-public-services) (6)
- [商業登記與金融財經 (Finance & Business)](#finance-business) (5)
- [天氣與環境水情 (Weather & Environment)](#weather-environment) (15)
- [交通與運輸 (Transportation)](#transportation) (8)
- [地理資訊與國土測繪 (Maps & Geospatial)](#maps-geospatial) (2)
- [文化與觀光 (Culture & Tourism)](#culture-tourism) (1)
- [教育與學術研究 (Education & Research)](#education-research) (1)
- [醫療與公共衛生 (Healthcare & Public Health)](#healthcare-public-health) (2)
- [開發者工具與輔助服務 (Developer Tools)](#developer-tools) (1)
- [其他開放服務 (Other)](#other) (0)

---

## 政府與公共服務 (Government & Public Services)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **中華郵政 3+3 郵遞區號查詢 Web Service**<br>`Chunghwa Post 3+3 Postal Code Query Web Service` | 中華郵政股份有限公司 | 提供台灣標準地址正規化與 3+3 郵遞區號查詢、縣市行政區反查之官方 SOAP Web Service 介面。 | `SOAP` | `other` | `free` | `yes` | `not_applicable` | `OGDL-Taiwan-1.0` | [文件連結](https://33wsp.post.gov.tw/LZWZIP/TZIP33.asmx) | `docs_reviewed` |
| **司法院資料開放平臺 API**<br>`Judicial Yuan Open Data Platform API` | 司法院 | 司法院官方資料開放平臺 RESTful API，提供全台各級法院裁判書、大法官解釋、憲法法庭判決與法規統計之分類清單與分頁資料查詢介面。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.judicial.gov.tw/DevelopmentGuide) | `endpoint_tested` |
| **高雄市垃圾車即時動態定位 API**<br>`Kaohsiung City Waste Truck Real-time GPS API` | 高雄市政府環境保護局 | 高雄市政府環境保護局提供之垃圾清運車輛即時 GPS 定位座標、車牌號碼、清運路線與即時行駛狀態查詢服務。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://openapi.kcg.gov.tw/) | `endpoint_tested` |
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
| **中央氣象署顯著有感與小區域地震報告 API**<br>`CWA Significant Felt & Local Earthquake Report API` | 交通部中央氣象署 | 中央氣象署官方即時發布之全台顯著有感地震與小區域地震報告，提供震央經緯度坐標、芮氏規模、震源深度與各縣市各測站即時最大震度。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dataset/earthquake/E-A0015-001) | `docs_reviewed` |
| **中央氣象署開放資料平台 API**<br>`CWA OpenData API` | 交通部中央氣象署 | 提供台灣氣象預報、即時天氣觀測、地震資訊與警報、氣象雷達及颱風警報資料之 RESTful 介面。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dist/opendata-swagger.html) | `docs_reviewed` |
| **中央氣象署雷達迴波即時圖資與降水估計 API**<br>`CWA Radar Echo Imagery & Precipitation Estimation API` | 交通部中央氣象署 | 中央氣象署全台防災氣象雷達網之即時合成雷達迴波圖資 (無地形/含地形)、彩色與黑白影像檔 URL 及定量降水估計 (QPE) 即時資料服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dataset/observation/O-A0058-001) | `docs_reviewed` |
| **中央氣象署即時雨量觀測與豪大雨特報 API**<br>`CWA Real-time Rainfall Observation & Heavy Rain Advisory API` | 交通部中央氣象署 | 中央氣象署全台自動雨量站之即時十分鐘、一小時、三小時、二十四小時累積雨量觀測，以及官方豪雨、大豪雨、超大豪雨特報警示資訊服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dataset/observation/O-A0002-001) | `docs_reviewed` |
| **中央氣象署全台三十六小時與鄉鎮天氣預報 API**<br>`CWA 36-Hour & Township Weather Forecast API` | 交通部中央氣象署 | 中央氣象署官方提供之全台各縣市三十六小時天氣預報、一週天氣預報與各鄉鎮市區逐三小時細部氣象預測數據 (涵蓋天氣現象、降雨機率、最高溫與最低溫)。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dataset/forecast/F-C0032-001) | `docs_reviewed` |
| **中央氣象署自動氣象站即時天氣觀測資料 API**<br>`CWA Automatic Weather Station Real-time Observation API` | 交通部中央氣象署 | 中央氣象署全台數百座地面氣象站與自動氣象站 (AWS) 之即時氣溫、相對濕度、十分鐘平均風速、瞬間最大陣風、氣壓與即時天氣現象觀測數值。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.cwa.gov.tw/dataset/observation/O-A0003-001) | `docs_reviewed` |
| **LASS AirBox 微型空氣品質感測器開源 API**<br>`LASS AirBox Micro-sensor Open API` | LASS 開源感測社群 | 由開源社群 LASS (Location Aware Sensing System) 與民間設備共同營運之全台微型環境感測網，每 5 分鐘提供全台數百個站點之 PM2.5、PM10、溫度與濕度即時數值。 | `REST` | `none` | `free` | `yes` | `yes` | `CC-BY-4.0` | [文件連結](https://pm25.lass-net.org/) | `endpoint_tested` |
| **環境部空氣品質監測 API**<br>`MOENV Air Quality API` | 環境部 | 提供全台各地測站即時空氣品質指標 (AQI)、PM2.5、PM10、臭氧及詳細大氣濃度數據。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/) | `docs_reviewed` |
| **環境部全台空氣品質指標 (AQI) 即時監測 API**<br>`MOENV National Air Quality Index (AQI) Real-time API` | 環境部 | 環境部空氣品質監測網提供之全國各官方測站即時空氣品質指標 (AQI)、PM2.5、PM10、O3、CO、SO2、NO2 濃度與空氣品質狀態等級。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/#/%E5%A4%A7%E6%B0%A3/get_aqx_p_432) | `docs_reviewed` |
| **環境部固定污染源連續自動監測 (CEMS) 即時連線 API**<br>`MOENV Continuous Emission Monitoring System (CEMS) Real-time API` | 環境部 | 環境部列管工廠煙囪固定污染源連續自動監測設施 (CEMS) 之即時連線排放數據，提供二氧化硫、氮氧化物、不透光率與排放流率監測資訊。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/#/%E5%A4%A7%E6%B0%A3/get_cems_p_01) | `docs_reviewed` |
| **環境部全台紫外線指數 (UVI) 即時觀測 API**<br>`MOENV National UV Index Real-time API` | 環境部 | 環境部大氣環境監測體系提供之全台主要測站紫外線即時指數 (UVI)、曝曬級數 (低量級至危險級) 與發布時間數據。 | `REST` | `api_key` | `free` | `yes` | `yes` | `OGDL-Taiwan-1.0` | [文件連結](https://data.moenv.gov.tw/swagger/#/%E5%A4%A7%E6%B0%A3/get_uv_p_01) | `docs_reviewed` |
| **水利署全台即時淹水警戒與感測資訊 API**<br>`WRA National Flood Early Warning & Sensor API` | 經濟部水利署 | 經濟部水利署依據短延時強降雨與即時雨量觀測發布之全國各鄉鎮市區一級與二級淹水警戒發布資訊，以及路面淹水感測器即時淹水深度。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.wra.gov.tw/openapi/swagger/index.html) | `docs_reviewed` |
| **水利署全台主要水庫即時蓄水量與水情 API**<br>`WRA National Reservoirs Real-time Water Storage API` | 經濟部水利署 | 經濟部水利署提供之全台主要水庫即時蓄水量、蓄水百分比、有效容量、水庫水位、本日進出水量與即時放水預警狀態服務。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.wra.gov.tw/openapi/swagger/index.html) | `docs_reviewed` |
| **水利署全國河川水位即時監測 API**<br>`WRA National River Water Level Real-time API` | 經濟部水利署 | 經濟部水利署全國主要中央管河川水位觀測站即時水位、各測站一級、二級與三級警戒水位數值與防汛警戒狀態查詢服務。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.wra.gov.tw/openapi/swagger/index.html) | `docs_reviewed` |
| **經濟部水利署水情與水利開放資料 API**<br>`WRA Water Resources Open Data & FHY API` | 經濟部水利署 | 提供水庫蓄水量、水情燈號、全台河川水位、淹水感測警戒與雨量站觀測數據。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://opendata.wra.gov.tw) | `docs_reviewed` |
## 交通與運輸 (Transportation)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **TDX 全國公車動態與路線資料 API**<br>`TDX National Bus Real-time Dynamics & Routes API` | 交通部 | 交通部運輸資料流通服務提供之全國市區公車與公路客運即時動態、路線站牌、預估到站時間與班表查詢服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/2998e851-81d0-40f5-b26d-77e2f5ac4118) | `docs_reviewed` |
| **TDX 全國機場即時航班起降資訊 API**<br>`TDX National Airport Flight Schedules & Status API` | 交通部 | 交通部民航局與各國際機場透過 TDX 提供之全國機場國內外航班預計與實際起降時間、航廈登機門、班機狀態與航空公司代碼查詢服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/2998e851-81d0-40f5-b26d-77e2f5ac4118) | `docs_reviewed` |
| **TDX 全國國道與快速道路即時路況 API**<br>`TDX Freeway Real-time Traffic & Speed API` | 交通部 | 交通部高公局與公路局透過 TDX 發布之全國高速公路與快速公路車輛偵測器 (VD) 即時車速、路段擁塞指標、旅行時間與即時路況事件。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/f5fbf756-3b95-4677-94ff-7faaa57697c1) | `docs_reviewed` |
| **TDX 全國都會區捷運路網與營運 API**<br>`TDX Urban Metro & MRT Systems API` | 交通部 | 交通部 TDX 整合之台北捷運、新北捷運、桃園捷運、台中捷運與高雄捷運全系統之車站資訊、路線幾何圖資、即時營運事件與列車班距服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/54ec8f08-0125-4c01-bf1a-fb80df8f000b) | `docs_reviewed` |
| **TDX 台灣高鐵列車時刻表與票價 API**<br>`TDX Taiwan High Speed Rail (THSR) Timetable & Fares API` | 交通部 | 交通部 TDX 提供之台灣高速鐵路全線車站資料、每日車次時刻表、車廂票價表與即時車次運行狀態查詢服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/54ec8f08-0125-4c01-bf1a-fb80df8f000b) | `docs_reviewed` |
| **TDX 臺灣鐵路列車動態與時刻表 API**<br>`TDX Taiwan Railway (TRA) Real-time Train Tracking API` | 交通部 | 交通部 TDX 提供之國營臺灣鐵路股份有限公司 (台鐵) 全線列車即時動態位置、準點與誤點分鐘數、列車時刻表與票價資訊服務。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/54ec8f08-0125-4c01-bf1a-fb80df8f000b) | `docs_reviewed` |
| **交通部運輸資料流通服務 (TDX)**<br>`Transport Data eXchange (TDX)` | 交通部 | 整合台灣軌道 (台鐵/高鐵/捷運)、公路客運、市區公車、公共自行車 (YouBike) 與航空船舶之全國即時動態與靜態路網資料。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger) | `docs_reviewed` |
| **TDX 全國公共自行車即時租借 API**<br>`TDX National Bike Sharing Real-time API` | 交通部 | 交通部 TDX 整合之全國公共自行車 (YouBike 2.0 / 共享單車) 各站點可借車輛數、可還空位數、站點座標與歷史營運狀態查詢介面。 | `REST` | `api_key` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://tdx.transportdata.tw/api-service/swagger/basic/2998e851-81d0-40f5-b26d-77e2f5ac4118) | `docs_reviewed` |
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

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **台北市立圖書館自修室座位即時狀態 API**<br>`TPML Study Room Real-time Seat Status API` | 台北市立圖書館 | 提供台北市立圖書館總館與各主要分館自修室之即時在館席位、剩餘座位與總座位數查詢介面。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://seat.tpml.edu.tw) | `endpoint_tested` |
## 醫療與公共衛生 (Healthcare & Public Health)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **健保署重度級急救責任醫院急診即時訊息 API**<br>`NHI Emergency Room Real-time Congestion API` | 衛生福利部中央健康保險署 | 提供全台重度級與兒童急救責任醫院即時急診等待就醫資訊，涵蓋等待掛號人數、等待看診人數、等待推床人數與等待加護病房人數之即時量能快照。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://info.nhi.gov.tw/INAE4000/INAE4001S01) | `endpoint_tested` |
| **食品藥物開放資料平臺 OpenAPI**<br>`TFDA Food and Drug Open Data OpenAPI` | 衛生福利部食品藥物管理署 | 衛生福利部食品藥物管理署提供之食品藥物開放資料 OpenAPI 服務，涵蓋全台西藥與中藥藥品許可證、健康食品、化妝品、醫療器材與食品營養資料庫之結構化規格。 | `REST` | `none` | `free` | `yes` | `unknown` | `OGDL-Taiwan-1.0` | [文件連結](https://data.fda.gov.tw/) | `endpoint_tested` |
## 開發者工具與輔助服務 (Developer Tools)

| API 名稱 | 提供者 | 簡介 | 類型 | 驗證機制 | 費用層級 | HTTPS | CORS | 上游授權 | 官方文件 | 查核等級 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **Twinkle Hub 台灣開放資料 MCP 閘道 API**<br>`Twinkle Hub Taiwan Open Data MCP Gateway` | Twinkle AI | 將台灣政府開放資料平台 (data.gov.tw) 數萬個資料集與發明專利、國考題庫、裁判書、藥品許可證與食品營養等五大語料庫，封裝為支援 AI Agent 結構化查詢之 Model Context Protocol (MCP) 介面。 | `RPC` | `api_key` | `free_tier` | `yes` | `unknown` | `CC-BY-4.0` | [文件連結](https://hub.twinkleai.tw/) | `endpoint_tested` |
## 其他開放服務 (Other)

*目前此分類尚無已審核通過之項目。*

---

## 附錄：待覆核與候選中項目 (Pending & Candidates)

> ⚠️ **注意**：以下項目尚未完成官方文件核實或端點測試，**未列入上方正式目錄主表**。僅供社群追蹤與後續查核。

| API 名稱 | 提供者 | 分類 | 審查狀態 | 說明與待辦備註 |
| :--- | :--- | :--- | :---: | :--- |
| **疾病管制署傳染病統計資料 API**<br>`Taiwan CDC Infectious Disease Surveillance API` | 衛生福利部疾病管制署 | Healthcare & Public Health | `needs_review` | 原登載之 `/applications/api` 端點返回 404 且自簽憑證異常；疾管署資料開放平台主要提供各傳染病固定 JSON/CSV 資源，特定資料集支援 CKAN Datastore API，待完成全面盤點與端點重測後再提升至 verified。 |
| **原住民族委員會開放資料 Datastore API**<br>`Council of Indigenous Peoples Open Data Datastore API` | 原住民族委員會 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描發現之原民會專屬 Datastore 端點。 |
| **人事行政總處天然災害停止上班及上課資訊 (歷次統計)**<br>`DGPA Disaster Work & School Cancellation Dataset` | 行政院人事行政總處 (DGPA) | Government & Public Services | `candidate` | 原登載之 data.gov.tw/dataset/26777 回應 500 且 base_url `/nds/opendata` 超時無法連線。人事行政總處官方即時公告多為網頁發布 (NDS HTML) 或歷次統計 CSV，缺乏官方長期維護之穩定公開 REST API 端點，保留為候選項目待確認。 |
| **桃園機場第一航廈入境人次預報 API**<br>`Taoyuan Airport Terminal 1 Arrival Passenger Forecast API` | 內政部移民署 | Transportation | `candidate` | 由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。 |
| **桃園機場第二航廈出境人次預報 API**<br>`Taoyuan Airport Terminal 2 Departure Passenger Forecast API` | 內政部移民署 | Transportation | `candidate` | 由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。 |
| **高雄市政府資料開放 OpenAPI 平台**<br>`Kaohsiung City Government OpenAPI Platform` | 高雄市政府 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描發現之地方政府標準 OpenAPI 平台。 |
| **內政部戶政司戶政資訊開放資料 API**<br>`Department of Household Registration Open Data API` | 內政部戶政司 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描 JSON/API 標籤發現，支援全國人口統計與路名即時查詢。 |
| **勞動部資料開放平臺 RESTful Datastore API**<br>`Ministry of Labor Open Data Service REST API` | 勞動部 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES (tid: 6413) 發現，收錄全平臺 Datastore 介面。 |
| **勞動基金主要金融市場指標 API**<br>`Labor Funds Key Financial Market Indicators API` | 勞動部勞動基金運用局 | Finance & Business | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES (nid: 30815) 自動產生之候選項目。 |
| **雇主聘僱外國人線上申辦量統計 API**<br>`Online Application Statistics for Employers Hiring Foreign Workers API` | 勞動部勞動力發展署 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES 自動產生之候選項目。 |
| **勞工體格及健康檢查認可醫療機構 API**<br>`Recognized Medical Institutions for Labor Health Examination API` | 勞動部職業安全衛生署 | Healthcare & Public Health | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES (nid: 6624) 自動產生之候選項目。 |
| **重大職業災害公開資訊 API**<br>`Major Occupational Disasters Public Information API` | 勞動部職業安全衛生署 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES (nid: 126835) 自動產生之候選項目。 |
| **台灣訓練品質系統 (TTQS) 效期內單位名單 API**<br>`Taiwan TrainQuali System (TTQS) Valid Accredited Units API` | 勞動部勞動力發展署 | Education & Research | `candidate` | 由 data.gov.tw 批次掃描 WEBSERVICES (nid: 41723) 自動產生之候選項目。 |
| **健保署特約醫療院所名冊資料集 (含介接)**<br>`NHI Contracted Medical Facilities Dataset` | 衛生福利部中央健康保險署 | Healthcare & Public Health | `needs_review` | 原登載之 dataset/21008 為急難救助基金之錯誤 ID，正確資料集為 168341；原登載之 data.nhi.gov.tw 主機已無法解析 DNS。健保署目前主要透過政府資料開放平台提供定期更新之 CSV/JSON 檔案與平台介接端點，待核實即時 API 規格後再提升至 verified。 |
| **臺南市政府開放資料服務導向 (SOA) API**<br>`Tainan City SOA Open Data API` | 臺南市政府 | Government & Public Services | `candidate` | 由 data.gov.tw 批次掃描發現，統一以 GUID 端點提供市政資料查詢。 |
| **台灣空氣品質歷史資料檢索 API (候選)**<br>`Taiwan Air Quality Historical Dataset API (Candidate)` | 環境部 | Weather & Environment | `candidate` | 歷史大量資料通常拆分為年別壓縮檔，API 僅支援小範圍分頁查詢，待完整評估後再決定是否升級為 verified。 |
| **安平港國際郵輪船期預報 API**<br>`Anping Port International Cruise Schedule Forecast API` | 臺灣港務股份有限公司 | Transportation | `candidate` | 由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。 |
| **臺中港兩岸渡輪船期預報 API**<br>`Taichung Port Cross-Strait Ferry Schedule Forecast API` | 臺灣港務股份有限公司 | Transportation | `candidate` | 由 data.gov.tw 批次掃描 API 標籤 (tid: 11519) 發現。 |
