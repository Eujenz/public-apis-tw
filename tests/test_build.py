import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_build_catalog_runner():
    script = ROOT / "scripts" / "build_catalog.py"
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert res.returncode == 0, f"build_catalog.py failed with stderr: {res.stderr}"

    catalog_md = ROOT / "docs" / "catalog.md"
    assert catalog_md.exists(), "docs/catalog.md must be generated"

    dist_json = ROOT / "dist" / "apis.json"
    assert dist_json.exists(), "dist/apis.json must be generated"
    with open(dist_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, list)
