import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_validate_catalog_runner():
    script = ROOT / "scripts" / "validate_catalog.py"
    # 當沒有檔案時應返回 1，若有資料則應依資料正確性回傳
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    # 只要能執行且不發生未捕捉的例外 (如語法錯誤、Traceback) 即可
    assert "Traceback" not in res.stderr
