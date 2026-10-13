# Public APIs Taiwan (public-apis-tw)

> 🇹🇼 A curated directory of APIs for building products in Taiwan.  
> 專為台灣開發者打造之公共與開放 API 精選目錄。

[![CI](https://github.com/public-apis-tw/public-apis-tw/actions/workflows/ci.yml/badge.svg)](https://github.com/public-apis-tw/public-apis-tw/actions/workflows/ci.yml)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE-CODE)
[![Catalog Data: CC BY 4.0](https://img.shields.io/badge/Catalog%20Data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

> 💡 **專案狀態說明**：本專案剛完成架構與第一版規格實作。上方 CI 徽章將在遠端 GitHub Repository 正式建立並推送後啟動運作。

---

## 🎯 專案目的與核心理念

本專案旨在為台灣開發者建立一份透明、客觀且具備可維護規格的開放與公共 API 目錄：

1. **區分 API 與靜態資料資源**：只收錄具有可程式化存取介面的服務，不將單純的 CSV、Excel、PDF 下載連結當作 API。但若靜態檔案是透過正式 API 端點取得，則依其實際介面與使用方式判定。
2. **規格與授權透明**：清楚揭露身分驗證方式（免金鑰 / API Key / OAuth）、計費層級（免費 / 免費額度）、CORS 支援度與上游個別授權條款（OGDL-Taiwan / CC 等）。
3. **客觀繁體中文**：以客觀中立之繁體中文描述功能與限制，保留原生官方技術術語與文件連結。
4. **誠實標示查核狀態**：嚴格區分「中繼資料已審閱 (docs_reviewed)」與「端點實際發送過請求測試 (endpoint_tested)」，未經實際測試絕不虛構填寫。

---

## 📖 完整目錄與資料檔案

- **結構化 Markdown 目錄**：請查閱 [📑 docs/catalog.md](docs/catalog.md) 查看依領域分類整理之完整表格。
- **機器可讀 JSON 檔案**：建置產出之全量資料位於 [📦 dist/apis.json](dist/apis.json)（納入版本庫追蹤）。
- **原始資料庫**：每一筆 API 均以單一 YAML 檔案獨立維護於 [📁 data/apis/](data/apis/) 目錄中。

---

## 🗂️ 領域分類索引 (Domain-Centric Categories)

目錄依照 API 之「主要使用領域」進行分類：

| 分類代碼 | 中文分類 | 範疇說明與候選方向 |
| :--- | :--- | :--- |
| **Government & Public Services** | 政府與公共服務 | 跨部會天然災害示警 (NCDR)、各縣市天然災害停班停課資訊、公用電力發電與備轉容量、各級政府開放資料入口等通用服務 |
| **Finance & Business** | 商業登記與金融財經 | 全國商工公司登記、上市櫃證券每日行情、電子發票開獎與查驗、農產品批發市場行情 |
| **Weather & Environment** | 天氣與環境水情 | 氣象預報、即時天氣觀測、地震資訊與警報、空氣品質監測 (AQI) 與水庫水情 |
| **Transportation** | 交通與運輸 | 交通部 TDX 整合平台 (鐵道、公路客運、市區公車、公共自行車、道路動態、航空船舶) |
| **Maps & Geospatial** | 地理資訊與國土測繪 | 內政部國土測繪圖資 (NLSC WMTS)、TGOS 全國門牌地址定位 (Geocoding) 與坐標轉換 |
| **Culture & Tourism** | 文化與觀光 | 觀光署全國景點活動、藝文展演、合法旅宿與觀光自行車道 |
| **Healthcare & Public Health** | 醫療與公共衛生 | 健保特約醫療院所與診療時段、疾管署法定傳染病統計監測 |
| **Developer Tools** | 開發者工具與輔助服務 | 台灣 3+3 郵遞區號剖析、中文地址正規化斷詞等在地開發工具 |
| **Education & Research** | 教育與學術研究 | 大專院校代碼、學術文獻期刊、研究機構典藏介面 |
| **Other** | 其他開放服務 | 其他具備在地開發價值之特色介面 |

> 註：上述範疇包含第一版正式收錄及後續擴充之研究方向，實際收錄項目請以 [docs/catalog.md](docs/catalog.md) 正式表格為準。

---

## 🛠️ 開發與本地建置

本專案採用 Python 3.12+ 與現代化套件管理工具 [uv](https://docs.astral.sh/uv/)。

### 1. 安裝環境
```bash
uv sync
```

### 2. 驗證資料目錄 (Schema、業務規則與狀態一致性檢驗)
```bash
uv run python scripts/validate_catalog.py
```

### 3. 執行測試套件
```bash
uv run pytest
```

### 4. 重新編譯 Markdown 目錄與 JSON
```bash
uv run python scripts/build_catalog.py
```

### 5. (選用) 檢查官方文件連結可達性
```bash
uv run python scripts/check_links.py
```

---

## 🤝 如何貢獻 (Contributing)

歡迎社群一同擴充收錄！新增一筆 API 僅需 4 個步驟：
1. 複製 `templates/api-template.yml` 至 `data/apis/<id>.yml`。
2. 填寫繁體中文名稱、描述、官方文件網址、驗證方式與上游授權。
3. 執行本地驗證與編譯：`uv run python scripts/validate_catalog.py` 與 `uv run python scripts/build_catalog.py`。
4. 送出 Pull Request。

詳細規範請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 與 [收錄政策文件](docs/catalog-policy.md)。

---

## ⚖️ 授權條款 (Licenses)

本專案採清楚拆分之授權模式：
- **建置腳本與專案程式碼**：採用 [MIT License](LICENSE-CODE)。
- **目錄彙整與詮釋資料**：採用 [CC BY 4.0 (創用 CC 姓名標示 4.0 國際)](LICENSE-DATA)，僅適用於本專案自行建立且有權授權之編目詮釋資料。
- **上游 API 資料之權利**：各 API 實際提供之資料、商標與服務均歸原機關法人所有，適用個別宣告之上游授權條款（如 OGDL-Taiwan 等），本目錄不作任何重新授權。
