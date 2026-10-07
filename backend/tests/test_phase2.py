import io
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.config import get_settings  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

KANNADA_OCR = (
    "ಕರ್ನಾಟಕ ಮಾರಾಟಪತ್ರ ದಾಖಲೆ. "
    "ಈ ಮಾರಾಟಪತ್ರದಲ್ಲಿ ನ್ಯಾಯಾಲಯದ ಪ್ರಕರಣ ಉಲ್ಲೇಖವಿದೆ."
)

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

CLEAN_SALE_DEED = """
SALE DEED
Seller: Anita
Buyer: Bharat
Survey Number: 10/2
This deed records a sale. No court papers are attached.
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


def upload_sale_deed(client: TestClient, headers: dict, filename: str = "SaleDeed.pdf") -> tuple[str, str]:
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "INDEPENDENT_HOUSE"},
        headers=headers,
    ).json()
    files = {"file": (filename, io.BytesIO(tiny_pdf()), "application/pdf")}
    document = client.post(f"/property-cases/{case['id']}/documents", files=files, headers=headers).json()
    return case["id"], document["id"]


def mock_sarvam(monkeypatch, original: str, translated: str | None = None, extract: dict | None = None):
    monkeypatch.setattr("app.services.analysis_service.digitise_document", lambda *args, **kwargs: original)
    monkeypatch.setattr(
        "app.services.analysis_service.translate_text",
        lambda *args, **kwargs: translated if translated is not None else original,
    )
    monkeypatch.setattr("app.services.analysis_service.extract_fields", lambda *args, **kwargs: extract or {})


def finding_by_category(payload: dict, category: str) -> dict:
    return next(item for item in payload["findings"] if item["category"] == category)


def test_analyze_requires_authentication(client: TestClient):
    response = client.post(f"/property-cases/{uuid4()}/documents/{uuid4()}/analyze")
    assert response.status_code == 401


def test_analyze_uploaded_pdf(client: TestClient, monkeypatch):
    mock_sarvam(
        monkeypatch,
        KANNADA_OCR,
        DEMO_ENGLISH,
        {"litigation": {"stay_order": None, "case_status": None, "case_number": None}},
    )
    headers = auth_header(client)
    case_id, document_id = upload_sale_deed(client, headers)
    response = client.post(f"/property-cases/{case_id}/documents/{document_id}/analyze", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["document_type"] == "SALE_DEED"
    assert body["analysis_status"] == "COMPLETE"
    assert body["translated_text"]
    assert "O.S. No. 234/2019" in body["translated_text"]
    litigation = finding_by_category(body, "LITIGATION")
    assert litigation["status"] == "DETECTED"
    assert litigation["risk_level"] == "HIGH"
    assert litigation["evidence"]
    assert finding_by_category(body, "MORTGAGE")["status"] == "NOT_VERIFIED"
    assert finding_by_category(body, "APPROVAL")["status"] == "NOT_VERIFIED"
    assert body["recommendations"]
    stored = client.get(f"/property-cases/{case_id}/documents/{document_id}/analysis", headers=headers)
    assert stored.status_code == 200
    assert stored.json()["id"] == body["id"]


def test_user_cannot_analyze_another_users_document(client: TestClient, monkeypatch):
    mock_sarvam(monkeypatch, KANNADA_OCR, DEMO_ENGLISH)
    owner = auth_header(client, "owner", "securePass1")
    case_id, document_id = upload_sale_deed(client, owner)
    other = auth_header(client, "intruder", "securePass1")
    response = client.post(f"/property-cases/{case_id}/documents/{document_id}/analyze", headers=other)
    assert response.status_code == 403


def test_missing_document_returns_404(client: TestClient):
    headers = auth_header(client)
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "VILLA"},
        headers=headers,
    ).json()
    response = client.post(
        f"/property-cases/{case['id']}/documents/11111111-1111-1111-1111-111111111111/analyze",
        headers=headers,
    )
    assert response.status_code == 404


def test_litigation_detected_from_explicit_evidence(client: TestClient, monkeypatch):
    mock_sarvam(monkeypatch, KANNADA_OCR, DEMO_ENGLISH, {"litigation": {"stay_order": None}})
    headers = auth_header(client)
    case_id, document_id = upload_sale_deed(client, headers)
    body = client.post(f"/property-cases/{case_id}/documents/{document_id}/analyze", headers=headers).json()
    litigation = finding_by_category(body, "LITIGATION")
    assert litigation["status"] == "DETECTED"
    assert "234/2019" in (litigation["finding_data"] or {}).get("case_number", "")
    assert (litigation["finding_data"] or {}).get("stay_order") is True
    evidence = client.get(f"/property-cases/{case_id}/evidence/{litigation['id']}", headers=headers)
    assert evidence.status_code == 200
    assert evidence.json()


def test_empty_evidence_does_not_produce_no_issue_found(client: TestClient, monkeypatch):
    mock_sarvam(monkeypatch, CLEAN_SALE_DEED, CLEAN_SALE_DEED)
    headers = auth_header(client)
    case_id, document_id = upload_sale_deed(client, headers)
    body = client.post(f"/property-cases/{case_id}/documents/{document_id}/analyze", headers=headers).json()
    assert finding_by_category(body, "LITIGATION")["status"] == "NOT_VERIFIED"
    assert finding_by_category(body, "MORTGAGE")["status"] == "NOT_VERIFIED"
    assert finding_by_category(body, "APPROVAL")["status"] == "NOT_VERIFIED"
    assert finding_by_category(body, "LITIGATION")["status"] != "NO_ISSUE_FOUND"


def test_recommendation_engine_returns_missing_documents(client: TestClient, monkeypatch):
    mock_sarvam(monkeypatch, KANNADA_OCR, DEMO_ENGLISH)
    headers = auth_header(client)
    case_id, document_id = upload_sale_deed(client, headers)
    client.post(f"/property-cases/{case_id}/documents/{document_id}/analyze", headers=headers)
    recs = client.get(f"/property-cases/{case_id}/recommendations", headers=headers)
    assert recs.status_code == 200
    types = {item["document_type"] for item in recs.json()}
    assert "ENCUMBRANCE_CERTIFICATE" in types
    assert "COURT_ORDER" in types
    assert "BUILDING_PLAN_APPROVAL" in types
