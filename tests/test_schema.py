import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent

def test_schema_itself_is_valid():
    schema_path = ROOT / "schemas" / "api.schema.json"
    assert schema_path.exists(), "Schema file must exist"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)

def test_schema_validates_valid_sample():
    schema_path = ROOT / "schemas" / "api.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    valid_record = {
        "id": "cwa-opendata",
        "name_zh": "中央氣象署開放資料平台 API",
        "description_zh": "提供台灣氣象預報、即時天氣觀測、地震資訊與警報之 RESTful 介面。",
        "category": "Weather & Environment",
        "provider": "交通部中央氣象署",
        "provider_type": "official",
        "docs_url": "https://opendata.cwa.gov.tw/dist/opendata-swagger.html",
        "api_style": "REST",
        "auth_type": "api_key",
        "access_tier": "free",
        "https_support": "yes",
        "cors_support": "yes",
        "license_name": "OGDL-Taiwan-1.0",
        "commercial_use": "allowed",
        "service_status": "active",
        "review_status": "verified",
        "verification_level": "docs_reviewed",
        "last_reviewed_at": "2026-10-13",
        "sources": [
            "https://opendata.cwa.gov.tw/"
        ]
    }
    assert validator.is_valid(valid_record)

def test_schema_rejects_missing_required_fields():
    schema_path = ROOT / "schemas" / "api.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    invalid_record = {
        "id": "missing-fields",
        "name_zh": "測試缺少欄位"
    }
    assert not validator.is_valid(invalid_record)
