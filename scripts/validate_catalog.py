#!/usr/bin/env python3
"""
validate_catalog.py - 驗證 public-apis-tw 目錄資料

檢查項目：
1. YAML 檔案是否能正常解析
2. 是否符合 JSON Schema (Draft 2020-12)
3. id 與檔名 stem 是否完全相符
4. id 是否唯一無重複
5. category 是否符合定義之領域分類
6. 網址格式與協定合理性 (docs_url 等必須以 http/https 開頭)
7. 狀態相容性與查核等級一致性：
   - review_status 為 verified 時：
     * 必須有 sources (至少 1 筆) 與 last_reviewed_at
     * verification_level 不得為 none (必須至少為 docs_reviewed)
   - verification_level 為 endpoint_tested 或 sample_response_checked 時：
     * 必須填寫 last_endpoint_tested_at
     * review_status 不得為 candidate
   - last_endpoint_tested_at 存在時，verification_level 不得為 none 或 docs_reviewed
8. 重複 docs_url 檢查並提出警告 (避免重複收錄，但允許共用文件入口之情境)
"""

import sys
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "apis"
SCHEMA_FILE = ROOT_DIR / "schemas" / "api.schema.json"

def main() -> int:
    print(f"[*] 載入 Schema: {SCHEMA_FILE}")
    if not SCHEMA_FILE.exists():
        print(f"[!] 找不到 Schema 檔案: {SCHEMA_FILE}", file=sys.stderr)
        return 1

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft202012Validator(schema)

    if not DATA_DIR.exists():
        print(f"[!] 找不到資料目錄: {DATA_DIR}", file=sys.stderr)
        return 1

    yaml_files = sorted(list(DATA_DIR.glob("*.yml")) + list(DATA_DIR.glob("*.yaml")))
    print(f"[*] 找到 {len(yaml_files)} 個 API 定義檔於 {DATA_DIR}")

    if not yaml_files:
        print("[!] 警告：目前沒有任何 API 檔案可供驗證。")
        return 1

    errors = []
    warnings = []
    seen_ids = set()
    seen_docs_urls = {}

    for file_path in yaml_files:
        rel_path = file_path.relative_to(ROOT_DIR)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            errors.append(f"{rel_path}: YAML 解析失敗 -> {e}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel_path}: 內容必須為鍵值對字典 (dict)")
            continue

        # 1. 檔名與 id 一致性
        expected_id = file_path.stem
        actual_id = data.get("id")
        if actual_id != expected_id:
            errors.append(f"{rel_path}: 'id' ({actual_id}) 與檔案名稱 stem ({expected_id}) 不符")

        # 2. 唯一性檢查
        if actual_id in seen_ids:
            errors.append(f"{rel_path}: 發現重複的 API ID: '{actual_id}'")
        else:
            seen_ids.add(actual_id)

        # 3. JSON Schema 結構校驗
        schema_errors = list(validator.iter_errors(data))
        for err in schema_errors:
            field = ".".join([str(p) for p in err.path]) or "<root>"
            errors.append(f"{rel_path} [{field}]: {err.message}")

        # 4. 業務邏輯校驗
        review_status = data.get("review_status")
        verification_level = data.get("verification_level")
        sources = data.get("sources", [])
        last_reviewed = data.get("last_reviewed_at")
        last_endpoint_tested = data.get("last_endpoint_tested_at")

        # review_status = verified 的相容條件
        if review_status == "verified":
            if not sources or len(sources) == 0:
                errors.append(f"{rel_path}: review_status 為 verified 時必須至少提供一筆來源 (sources)")
            if not last_reviewed:
                errors.append(f"{rel_path}: review_status 為 verified 時必須填寫 last_reviewed_at")
            if verification_level == "none":
                errors.append(f"{rel_path}: review_status 為 verified 但 verification_level 為 none，邏輯不符 (已審查通過者至少需為 docs_reviewed)")

        # verification_level 與 last_endpoint_tested_at 的約束
        if verification_level in ("endpoint_tested", "sample_response_checked"):
            if review_status == "candidate":
                errors.append(f"{rel_path}: verification_level 為 {verification_level} 但 review_status 仍為 candidate，邏輯不符")
            if not last_endpoint_tested:
                errors.append(f"{rel_path}: verification_level 為 {verification_level} 時必須明確填寫 last_endpoint_tested_at")
        elif last_endpoint_tested:
            errors.append(f"{rel_path}: 已填寫 last_endpoint_tested_at，但 verification_level 仍為 {verification_level}，應提升為 endpoint_tested 或更高")

        # 5. 重複 docs_url 警告 (共用入口提示)
        docs_url = data.get("docs_url")
        if docs_url:
            if docs_url in seen_docs_urls:
                warnings.append(
                    f"警告: {rel_path} 與 {seen_docs_urls[docs_url]} 使用相同的 docs_url ({docs_url})"
                )
            else:
                seen_docs_urls[docs_url] = rel_path

    if warnings:
        print("\n--- 警告清單 (非阻礙性) ---")
        for w in warnings:
            print(f"[WARN] {w}")

    if errors:
        print(f"\n[X] 驗證失敗！共發現 {len(errors)} 個錯誤：", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"\n[V] 驗證通過！共成功檢查 {len(yaml_files)} 個 API 檔案，無格式或邏輯相容性錯誤。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
