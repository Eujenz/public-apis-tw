import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from scrape_api_docs import infer_formats, extract_base_url, infer_auth_type, build_entry_yaml
from validate_catalog import validate_entry

def test_infer_formats_empty_when_no_declarations():
    """當 OpenAPI 規格中無任何 produces/consumes/content 宣告時，不可預設為 JSON，應回傳空清單"""
    spec = {"openapi": "3.0.0", "info": {"title": "Test"}}
    formats = infer_formats(spec)
    assert formats == [], f"預期未宣告時回傳空清單，但得到: {formats}"

def test_infer_formats_detects_json_and_xml():
    """當規格宣告 JSON 與 XML 時，能正確提取格式"""
    spec = {
        "produces": ["application/json", "application/xml"],
        "paths": {}
    }
    formats = infer_formats(spec)
    assert formats == ["JSON", "XML"]

def test_extract_base_url_returns_none_when_no_server_info():
    """規格缺少 servers 或 host 時，嚴禁退回 doc_url 的主機名稱，必須回傳 None"""
    spec = {"openapi": "3.0.0", "info": {"title": "No Server Spec"}}
    doc_url = "https://doc-portal.example.com/swagger/index.html"
    base_url = extract_base_url(spec, doc_url)
    assert base_url is None, f"預期回傳 None，但得到: {base_url}"

def test_extract_base_url_extracts_openapi3_server():
    """能正確提取 OpenAPI 3 中的伺服器 URL"""
    spec = {
        "openapi": "3.0.0",
        "servers": [{"url": "https://api.example.com/v1"}]
    }
    base_url = extract_base_url(spec, "https://docs.example.com")
    assert base_url == "https://api.example.com/v1"

def test_infer_auth_type_returns_none_when_no_security():
    """無任何 securityDefinitions/securitySchemes 宣告時，回傳 none"""
    spec = {"swagger": "2.0", "info": {"title": "Open API"}}
    assert infer_auth_type(spec) == "none"

def test_infer_auth_type_detects_api_key():
    """能辨識 apiKey 定義"""
    spec = {
        "swagger": "2.0",
        "securityDefinitions": {
            "ApiKeyAuth": {"type": "apiKey", "name": "X-API-KEY", "in": "header"}
        }
    }
    assert infer_auth_type(spec) == "api_key"

def test_build_entry_yaml_is_always_candidate():
    """自動爬蟲生成的 YAML 條目必須始終標記為 candidate 且 verification_level 為 none"""
    doc_url = "https://example.gov.tw/api/docs"
    entry = build_entry_yaml(doc_url, captured_specs=[], page_metadata={"title": "自動推論 API"})
    assert entry["review_status"] == "candidate"
    assert entry["verification_level"] == "none"
    assert "待人工覆核" in entry["notes"]
    assert "base_url" not in entry or entry.get("base_url") is None
