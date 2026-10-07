import io
import json
import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.config import get_settings  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.report import FinalReport  # noqa: E402
from app.services.comparison_service import values_match  # noqa: E402
from app.services.extraction_service import fallback_from_source  # noqa: E402
from app.services.hashing import hash_payload  # noqa: E402

KANNADA_OCR = "ಕರ್ನಾಟಕ ಮಾರಾಟಪತ್ರ ದಾಖಲೆ."

DEMO_ENGLISH = """
SALE DEED
Seller: Ramesh
Buyer: Suresh
Survey Number: 45/3
Area: 1200 sq ft
Village: Hebbala
Hobli: Yelahanka
Taluk: Bengaluru North
District: Bengaluru
State: Karnataka
Sale Amount: Rs 45 lakh
Previous Deed: 1823/2015
Case O.S. No. 234/2019 is pending before City Civil Court Bengaluru.
Stay Order is in force.
Transfer/alienation is restricted.
"""

EC_CLEAR = """
ENCUMBRANCE CERTIFICATE
Survey Number: 45/3
Village: Hebbala
This certificate records nil encumbrance for the search period.
No encumbrance. No dues.
"""

SURVEY_MATCH = """
SURVEY SKETCH
Sy. No. 45/3
Area: 1200 sq ft
Village: Hebbala
"""

SURVEY_MISMATCH = """
SURVEY SKETCH
Survey Number: 45/4
Area: 1200 sq ft
Village: Hebbala
"""

KHATA_AREA_MISMATCH = """
KHATA / PROPERTY REGISTER
Survey Number: 45/3
Area: 1000 sq ft
Village: Hebbala
"""

APPROVAL_CLEAR = """
BUILDING PLAN APPROVAL
Approval present. Approval number BBMP/2020/88.
Occupancy certificate is present.
Village: Hebbala
Survey Number: 45/3
"""


@pytest.fixture()
def client(tmp_path, monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    storage = tmp_path / "documents"
    storage.mkdir()
    settings = get_settings()
    monkeypatch.setattr(settings, "STORAGE_DIR", storage)
    monkeypatch.setattr(settings, "MAX_FILE_SIZE_MB", 1)
    monkeypatch.setattr(settings, "SARVAM_API_KEY", "test-key")

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.state.skip_db_init = True
    with TestClient(app) as test_client:
        test_client.session_factory = TestingSession
        yield test_client
    app.dependency_overrides.clear()
    app.state.skip_db_init = False


def signup(client: TestClient, username: str = "advocate", password: str = "securePass1"):
    return client.post(
        "/auth/signup",
        json={"username": username, "password": password, "confirm_password": password},
    )


def login(client: TestClient, username: str = "advocate", password: str = "securePass1"):
    return client.post("/auth/login", json={"username": username, "password": password})


def auth_header(client: TestClient, username: str = "advocate", password: str = "securePass1") -> dict[str, str]:
    signup(client, username, password)
    token = login(client, username, password).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def tiny_pdf() -> bytes:
    return b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def create_case(client: TestClient, headers: dict) -> str:
    return client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "INDEPENDENT_HOUSE"},
        headers=headers,
    ).json()["id"]


def upload(client: TestClient, headers: dict, case_id: str, filename: str) -> str:
    files = {"file": (filename, io.BytesIO(tiny_pdf()), "application/pdf")}
    return client.post(f"/property-cases/{case_id}/documents", files=files, headers=headers).json()["id"]


def mock_sarvam_map(monkeypatch, mapping: dict[str, tuple[str, str]]):
    def digitise(_path, filename, *_args, **_kwargs):
        return mapping[filename][0]

    def translate(text, *_args, **_kwargs):
        for original, translated in mapping.values():
            if text == original:
                return translated
        return text

    monkeypatch.setattr("app.services.analysis_service.digitise_document", digitise)
    monkeypatch.setattr("app.services.analysis_service.translate_text", translate)
    monkeypatch.setattr("app.services.analysis_service.extract_fields", lambda *args, **kwargs: {})


def finding(payload: dict, category: str) -> dict:
    return next(item for item in payload["findings"] if item["category"] == category)


INCOMPLETE_OWNERSHIP = """
SALE DEED
Survey Number: 45/3
Village: Hebbala
This deed records a sale. Names of the parties are not printed clearly.
"""

LITIGATION_DEED_EN = """
This full deed was prepared and executed on the 15th of March, 2024 (15.03.2024) in Bangalore by:
Sri. Ramachandra Prasad
Father: Sri. Venkataramana Prasad,
Age: Approximately 52 years,
Further referred to as 'One Party Seller'.
Deed in favour of:
Sri. Arjun Kumar Shetty
Father: Sri. Mohan Shetty,
Survey Number: 45/3
The seller acquired the property through purchase deed number 1823/2015.
"""

LITIGATION_DEED_KN = """
ಈ ಸಂಪೂರ್ಣ ಕ್ರಯಪತ್ರವನ್ನು ತಯಾರಿಸಿ ಕಾರ್ಯಗತಗೊಳಿಸಲಾಗಿದೆ, ಇವರಿಂದ:
ಶ್ರೀ. ರಾಮಚಂದ್ರ ಪ್ರಸಾದ್
ತಂದೆ: ಶ್ರೀ. ವೆಂಕಟರಮಣ ಪ್ರಸಾದ್,
ಪರವಾಗಿ:
ಶ್ರೀ. ಅರ್ಜುನ್ ಕುಮಾರ್ ಶೆಟ್ಟಿ
ತಂದೆ: ಶ್ರೀ. ಮೋಹನ್ ಶೆಟ್ಟಿ,
"""


def test_extracts_party_names_from_executed_by_sale_deed():
    data = fallback_from_source(LITIGATION_DEED_EN)
    assert data["ownership"]["seller_name"] == "Sri. Ramachandra Prasad"
    assert data["ownership"]["buyer_name"] == "Sri. Arjun Kumar Shetty"
    assert data["transaction"]["previous_deed_number"] == "1823/2015"


def test_extracts_party_names_from_kannada_sale_deed():
    data = fallback_from_source(LITIGATION_DEED_KN)
    assert "ರಾಮಚಂದ್ರ" in (data["ownership"]["seller_name"] or "")
    assert "ಅರ್ಜುನ್" in (data["ownership"]["buyer_name"] or "")


def test_ownership_incomplete_attaches_source_evidence(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (INCOMPLETE_OWNERSHIP, INCOMPLETE_OWNERSHIP)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    body = client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers).json()
    ownership = finding(body, "OWNERSHIP")
    assert ownership["status"] == "DETECTED"
    texts = " ".join(item.get("source_text") or "" for item in ownership["evidence"])
    assert ownership["evidence"]
    assert "45/3" in texts
    assert "seller" in texts.lower() or "buyer" in texts.lower()


def test_ownership_reads_names_from_indian_sale_deed(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (LITIGATION_DEED_KN, LITIGATION_DEED_EN)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    body = client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers).json()
    ownership = finding(body, "OWNERSHIP")
    details = ownership["finding_data"] or {}
    assert details.get("seller_name") == "Sri. Ramachandra Prasad"
    assert details.get("buyer_name") == "Sri. Arjun Kumar Shetty"
    assert ownership["status"] != "DETECTED"
    texts = " ".join(item.get("source_text") or "" for item in ownership["evidence"])
    assert "Ramachandra" in texts
    assert "Arjun" in texts


def test_values_match_normalizes_survey_prefixes():
    assert values_match("survey_number", "Survey No. 45/3", "Sy. No. 45/3")
    assert values_match("survey_number", "Survey Number: 45/3", "45/3")
    assert not values_match("survey_number", "45/3", "45/4")
    assert values_match("area", "1200 sq ft", "1,200 square feet")
    assert not values_match("seller_name", "Ramesh", "Suresh")


def test_multiple_documents_belong_to_one_case(client: TestClient):
    headers = auth_header(client)
    case_id = create_case(client, headers)
    first = upload(client, headers, case_id, "SaleDeed.pdf")
    second = upload(client, headers, case_id, "EC.pdf")
    listed = client.get(f"/property-cases/{case_id}/documents", headers=headers)
    assert listed.status_code == 200
    ids = {item["id"] for item in listed.json()}
    assert first in ids and second in ids
    assert len(listed.json()) == 2


def test_matching_survey_numbers_are_match(client: TestClient, monkeypatch):
    mock_sarvam_map(
        monkeypatch,
        {
            "SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH),
            "Survey.pdf": (SURVEY_MATCH, SURVEY_MATCH),
        },
    )
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    sketch = upload(client, headers, case_id, "Survey.pdf")
    assert client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers).status_code == 200
    assert client.post(f"/property-cases/{case_id}/documents/{sketch}/analyze", headers=headers).status_code == 200
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    survey = [row for row in body["comparisons"] if row["field"] == "survey_number"]
    assert any(row["result"] == "MATCH" for row in survey)


def test_different_survey_numbers_are_mismatch(client: TestClient, monkeypatch):
    mock_sarvam_map(
        monkeypatch,
        {
            "SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH),
            "Survey.pdf": (SURVEY_MISMATCH, SURVEY_MISMATCH),
        },
    )
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    sketch = upload(client, headers, case_id, "Survey.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    client.post(f"/property-cases/{case_id}/documents/{sketch}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    survey = next(row for row in body["mismatches"] if row["field"] == "survey_number")
    assert survey["result"] == "MISMATCH"
    assert survey["severity"] == "HIGH"
    assert finding(body, "PROPERTY_RECORD")["status"] == "DETECTED"


def test_different_areas_are_mismatch(client: TestClient, monkeypatch):
    mock_sarvam_map(
        monkeypatch,
        {
            "SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH),
            "Khata.pdf": (KHATA_AREA_MISMATCH, KHATA_AREA_MISMATCH),
        },
    )
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    khata = upload(client, headers, case_id, "Khata.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    client.post(f"/property-cases/{case_id}/documents/{khata}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    area = next(row for row in body["mismatches"] if row["field"] == "area")
    assert area["result"] == "MISMATCH"
    assert "1200" in area["value_a"] or "1200" in area["value_b"]
    assert "1000" in area["value_a"] or "1000" in area["value_b"]


def test_recalculation_uses_all_uploaded_documents(client: TestClient, monkeypatch):
    mock_sarvam_map(
        monkeypatch,
        {
            "SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH),
            "EC.pdf": (EC_CLEAR, EC_CLEAR),
        },
    )
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    ec = upload(client, headers, case_id, "EC.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    client.post(f"/property-cases/{case_id}/documents/{ec}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    assert body["analyzed_document_count"] == 2
    assert finding(body, "LITIGATION")["status"] == "DETECTED"
    assert finding(body, "MORTGAGE")["status"] == "NO_ISSUE_FOUND"


def test_mortgage_clears_when_ec_has_nil_encumbrance(client: TestClient, monkeypatch):
    mock_sarvam_map(
        monkeypatch,
        {
            "SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH),
            "EC.pdf": (EC_CLEAR, EC_CLEAR),
        },
    )
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    first = client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers).json()
    assert finding(first, "MORTGAGE")["status"] == "NOT_VERIFIED"
    ec = upload(client, headers, case_id, "EC.pdf")
    client.post(f"/property-cases/{case_id}/documents/{ec}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    assert finding(body, "MORTGAGE")["status"] == "NO_ISSUE_FOUND"


def test_missing_evidence_remains_not_verified(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    assert finding(body, "MORTGAGE")["status"] == "NOT_VERIFIED"
    assert finding(body, "APPROVAL")["status"] == "NOT_VERIFIED"
    assert finding(body, "MORTGAGE")["status"] != "NO_ISSUE_FOUND"


def test_verification_coverage_is_calculated(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    body = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    coverage = body["verification_coverage"]
    assert 0 <= coverage["percent"] <= 100
    assert coverage["categories"]
    assert "not a safety guarantee" in coverage["explanation"].lower()


def test_risk_score_is_deterministic(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    first = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    second = client.post(f"/property-cases/{case_id}/recalculate", headers=headers).json()
    assert first["risk_score"] == second["risk_score"]
    assert first["risk_level"] == second["risk_level"]
    assert first["risk_score"] == 70
    assert first["risk_level"] == "HIGH"
    reasons = first.get("score_reasons") or []
    assert any(item.get("reason") == "Litigation on the property" for item in reasons)


def test_final_report_hash_and_ledger(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    created = client.post(f"/property-cases/{case_id}/finalize", headers=headers)
    assert created.status_code == 200
    report = created.json()
    assert report["version"] == 1
    assert report["report_hash"]
    assert report["report_hash"] == hash_payload(report["report_content"])
    assert report["ledger"]["previous_hash"] == "GENESIS"
    assert report["ledger"]["record_hash"]
    listed = client.get(f"/property-cases/{case_id}/reports", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == report["id"]


def test_second_report_links_to_previous_hash(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    first = client.post(f"/property-cases/{case_id}/finalize", headers=headers).json()
    second = client.post(f"/property-cases/{case_id}/finalize", headers=headers).json()
    assert second["version"] == 2
    assert second["ledger"]["previous_hash"] == first["ledger"]["record_hash"]


def test_untouched_report_passes_integrity_verification(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    report = client.post(f"/property-cases/{case_id}/finalize", headers=headers).json()
    verify = client.get(f"/property-cases/{case_id}/reports/{report['id']}/verify", headers=headers)
    assert verify.status_code == 200
    body = verify.json()
    assert body["status"] == "VALID"
    assert body["report_hash_valid"] is True
    assert body["ledger_valid"] is True
    assert body["chain_valid"] is True


def test_modified_report_fails_integrity_verification(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    headers = auth_header(client)
    case_id = create_case(client, headers)
    deed = upload(client, headers, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=headers)
    report = client.post(f"/property-cases/{case_id}/finalize", headers=headers).json()
    db = client.session_factory()
    try:
        row = db.get(FinalReport, UUID(report["id"]))
        content = json.loads(json.dumps(row.report_content))
        content["property_information"]["survey_number"] = "TAMPERED"
        row.report_content = content
        flag_modified(row, "report_content")
        db.commit()
    finally:
        db.close()
    verify = client.get(f"/property-cases/{case_id}/reports/{report['id']}/verify", headers=headers).json()
    assert verify["status"] == "TAMPERED"
    assert verify["report_hash_valid"] is False


def test_unauthorized_user_cannot_access_report(client: TestClient, monkeypatch):
    mock_sarvam_map(monkeypatch, {"SaleDeed.pdf": (KANNADA_OCR, DEMO_ENGLISH)})
    owner = auth_header(client, "owner", "securePass1")
    case_id = create_case(client, owner)
    deed = upload(client, owner, case_id, "SaleDeed.pdf")
    client.post(f"/property-cases/{case_id}/documents/{deed}/analyze", headers=owner)
    report = client.post(f"/property-cases/{case_id}/finalize", headers=owner).json()
    other = auth_header(client, "intruder", "securePass1")
    assert client.get(f"/property-cases/{case_id}/reports/{report['id']}", headers=other).status_code == 403
    assert client.post(f"/property-cases/{case_id}/recalculate", headers=other).status_code == 403
    assert client.post(f"/property-cases/{uuid4()}/recalculate", headers=owner).status_code == 404
    assert client.post(f"/property-cases/{case_id}/recalculate").status_code == 401
