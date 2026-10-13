## 變更摘要 (Summary of Changes)

請簡述本次 Pull Request 的修改內容（新增 API / 修正資訊 / 更新工具等）：

## 檢核清單 (Checklist)

請在送出 PR 前逐項確認：

- [ ] 若為新增或修改 API，檔案已依照 `templates/api-template.yml` 格式置於 `data/apis/<id>.yml`。
- [ ] 該 API 具有明確之官方技術文件與來源，符合 [Catalog Policy](docs/catalog-policy.md)。
- [ ] 未經實際發起 HTTP 請求測試者，未將 `verification_level` 標記為 `endpoint_tested`。
- [ ] 已於本地端執行並通過驗證指令：
  ```bash
  uv run python scripts/validate_catalog.py
  uv run pytest
  uv run python scripts/build_catalog.py
  ```
- [ ] `docs/catalog.md` 與 `dist/apis.json` 已同步更新。
- [ ] PR 中不包含任何私有 API Key、Token 或機敏資訊。
