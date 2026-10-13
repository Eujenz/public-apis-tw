# Public APIs Taiwan (public-apis-tw)

> 🇹🇼 A curated directory of APIs for building products in Taiwan.  
> 專為台灣開發者打造之公共與開放 API 精選目錄。

[![CI](https://github.com/public-apis-tw/public-apis-tw/actions/workflows/ci.yml/badge.svg)](https://github.com/public-apis-tw/public-apis-tw/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## 🎯 專案目的與核心理念

本專案旨在解決台灣開發者在尋找開放資料與即時 API 時常面臨的痛點：
1. **區分真假 API**：嚴格過濾純靜態檔案（CSV、Excel、PDF），僅收錄具備 HTTP/RESTful 等可程式化查詢介面的服務。
2. **規格與授權透明**：清楚揭露身分驗證方式（免金鑰 / API Key / OAuth）、計費層級（免費 / 免費額度）、CORS 支援度與授權條款（OGDL-Taiwan / CC 等）。
3. **客觀繁體中文**：以台灣工程師熟悉的語言與名詞客觀說明，附帶官方原生文件連結。
4. **誠實標示查核狀態**：嚴格區分「已審閱文件 (docs_reviewed)」與「端點實際發送過請求測試 (endpoint_tested)」，拒絕憑空捏造資訊。

---

## 📖 完整目錄與資料檔案

- **結構化 Markdown 目錄**：請查閱 [📑 docs/catalog.md](docs/catalog.md) 查看依分類排列的完整表格。
- **機器可讀 JSON 檔案**：建置產出之全量資料位於 [📦 dist/apis.json](dist/apis.json)。
- **原始資料庫**：每一筆 API 均獨立維護於 [📁 data/apis/](data/apis/) 內的 YAML 檔案。

---

## 🗂️ 分類索引

| 分類代碼 | 中文分類 | 簡介 |
| :--- | :--- | :--- |
| **Government** | 政府與公共資訊 | 跨部會天然災害警報 (NCDR)、停班停課資訊、公用電力與地方政府開放資料庫 |
| **Finance & Business** | 商業登記與金融財經 | 全國商工登記、證券交易所 (TWSE/TPEx) 行情、電子發票與農產交易行情 |
| **Weather & Environment** | 天氣與環境水情 | 中央氣象署 (CWA) 預報地震、環境部空氣品質 (AQI) 與水利署水庫水情 |
| **Transportation** | 交通與運輸 | 交通部 TDX 整合平台 (鐵道、公路、公車、YouBike、航空) |
| **Maps & Geospatial** | 地理資訊與國土測繪 | 內政部國土測繪圖資 (NLSC WMTS)、TGOS 全國門牌地址定位 (Geocoding) |
| **Culture & Tourism** | 文化與觀光 | 觀光署全台景點活動、旅宿餐飲與自行車道開放資料 |
| **Healthcare & Public Health**| 醫療與公共衛生 | 健保署特約院所與就醫時段、疾管署法定傳染病監測統計 |
| **Developer Tools** | 開發者工具與輔助服務 | 台灣 3+3 郵遞區號與中文地址斷詞等社群微服務 |
| **Education & Research** | 教育與學術研究 | 大專院校、學術文獻與研究機構開放介面 |
| **Other** | 其他開放服務 | 其他具備在地價值之開放介面 |

---

## 🛠️ 開發與本地建置

本專案採用 Python 3.12+ 與現代化套件管理工具 [uv](https://docs.astral.sh/uv/)。

### 安裝環境
```bash
# 複製專案後同步虛擬環境與開發依賴
uv sync --extra dev
```

### 驗證目錄資料 (Schema & 業務規則檢驗)
```bash
uv run python scripts/validate_catalog.py
```

### 執行單元與整合測試
```bash
uv run pytest
```

### 重新編譯 Markdown 目錄與 JSON
```bash
uv run python scripts/build_catalog.py
```

### (選用) 檢查官方文件連結存取狀態
```bash
uv run python scripts/check_links.py
```

---

## 🤝 如何貢獻 (Contributing)

歡迎社群一同擴充收錄！新增一筆 API 僅需 4 個步驟：
1. 複製 `templates/api-template.yml` 至 `data/apis/<id>.yml`。
2. 填寫繁體中文名稱、描述、官方文件網址與驗證方式。
3. 執行本地驗證 `uv run python scripts/validate_catalog.py` 與 `uv run python scripts/build_catalog.py`。
4. 送出 Pull Request。

詳細規範請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 與 [收錄政策文件](docs/catalog-policy.md)。

---

## ⚖️ 授權條款 (License)

本專案採雙重授權：
- **程式碼、Schema 與建置腳本**：採用 [MIT License](LICENSE)。
- **目錄彙整中繼資料與文件**：採用 [CC BY 4.0 (創用 CC 姓名標示 4.0 國際)](LICENSE)。

各收錄之 API 與其商標、官方資料權益均歸原提供單位所有。
