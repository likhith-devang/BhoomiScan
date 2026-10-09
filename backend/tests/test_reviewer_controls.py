"""Reviewer controls: property-only AI, English validation, RBAC, discard, audit, F1 metrics.

Tests follow the property workflow order:
1) auth → 2) case → 3) upload → 4) gate/analyze → 5) finalize/discard → 6) roles/PDF → 7) metrics
"""

import io
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.config import get_settings  # noqa: E402
from app.constants import (  # noqa: E402
    DOCUMENT_STATUS_DISCARDED,
    ROLE_ADMIN,
    ROLE_BUYER,
    ROLE_SECONDARY_ADMIN,
    ROLE_SUPER_ADMIN,
)
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.audit import AuditLog  # noqa: E402
from app.models.document import Document  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.metrics_service import binary_scores  # noqa: E402
from app.services.property_gate import is_property_document, validate_english_working_text  # noqa: E402
from app.constants import ENGLISH_LANGUAGE  # noqa: E402

SALE_DEED = """
SALE DEED
Seller: Ramesh Kumar
Buyer: Suresh Rao
Survey Number: 45/3
Area: 1200 sq ft
Village: Hebbala
Hobli: Yelahanka
Taluk: Bengaluru North
District: Bengaluru
State: Karnataka
This deed records a sale of the schedule property.
"""

RESUME = """
Curriculum Vitae
John Doe
Software Engineer
Education: B.Tech Computer Science
Work experience at ACME Corp.
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
        test_client.storage_dir = storage
        yield test_client
    app.dependency_overrides.clear()
    app.state.skip_db_init = False


def signup(client: TestClient, username: str, password: str = "securePass1"):
    return client.post(
        "/auth/signup",
        json={"username": username, "password": password, "confirm_password": password},
    )


def login(client: TestClient, username: str, password: str = "securePass1"):
    return client.post("/auth/login", json={"username": username, "password": password})


def auth_header(client: TestClient, username: str, password: str = "securePass1") -> dict[str, str]:
    signup(client, username, password)
    token = login(client, username, password).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def set_role(client: TestClient, username: str, role: str) -> None:
    db = client.session_factory()
    try:
        user = db.scalar(select(User).where(User.username == username))
        user.role = role
        db.commit()
    finally:
        db.close()


def relogin(client: TestClient, username: str, password: str = "securePass1") -> dict[str, str]:
    token = login(client, username, password).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def tiny_pdf() -> bytes:
    return b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def mock_text(monkeypatch, text: str):
    monkeypatch.setattr("app.services.analysis_service.digitise_document", lambda *a, **k: text)
    monkeypatch.setattr("app.services.analysis_service.translate_text", lambda t, *a, **k: t)
    monkeypatch.setattr("app.services.analysis_service.extract_fields", lambda *a, **k: {})


# --- 1. Auth / role defaults ---


def test_01_signup_defaults_to_buyer_role(client: TestClient):
    response = signup(client, "buyer1")
    assert response.status_code == 201
    assert response.json()["role"] == ROLE_BUYER
    me = client.get("/auth/me", headers=auth_header(client, "buyer1b"))
    # auth_header already signed up buyer1b
    assert me.status_code == 200
    assert me.json()["role"] == ROLE_BUYER


# --- 2–3. Property case + upload ---


def test_02_property_case_then_document_upload(client: TestClient):
    headers = auth_header(client, "flow_user")
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "APARTMENT_FLAT"},
        headers=headers,
    )
    assert case.status_code == 201
    case_id = case.json()["id"]
    upload = client.post(
        f"/property-cases/{case_id}/documents",
        files={"file": ("SaleDeed.pdf", io.BytesIO(tiny_pdf()), "application/pdf")},
        headers=headers,
    )
    assert upload.status_code == 201
    assert upload.json()["status"] == "UPLOADED"


# --- 4. Property gate + English validation ---


def test_03_property_gate_rejects_non_property_files():
    ok, reason = is_property_document("OTHER", RESUME, "resume.pdf")
    assert ok is False
    assert "property" in reason.lower()


def test_04_property_gate_accepts_sale_deed():
    ok, _ = is_property_document("SALE_DEED", SALE_DEED, "SaleDeed.pdf")
    assert ok is True


def test_05_english_document_validation():
    result = validate_english_working_text(SALE_DEED, ENGLISH_LANGUAGE)
    assert result["ok"] is True
    thin = validate_english_working_text("ok", ENGLISH_LANGUAGE)
    assert thin["ok"] is False
    short_sketch = validate_english_working_text(
        "SURVEY SKETCH Sy. No. 45/3 Village Hebbala",
        ENGLISH_LANGUAGE,
        classified_property_type=True,
    )
    assert short_sketch["ok"] is True


def test_06_analyze_rejects_non_property_upload(client: TestClient, monkeypatch):
    mock_text(monkeypatch, RESUME)
    headers = auth_header(client, "gate_user")
    case_id = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "VILLA"},
        headers=headers,
    ).json()["id"]
    doc_id = client.post(
        f"/property-cases/{case_id}/documents",
        files={"file": ("resume.pdf", io.BytesIO(tiny_pdf()), "application/pdf")},
        headers=headers,
    ).json()["id"]
    body = client.post(f"/property-cases/{case_id}/documents/{doc_id}/analyze", headers=headers).json()
    assert body["analysis_status"] == "FAILED"
    docs = client.get(f"/property-cases/{case_id}/documents", headers=headers).json()
    assert docs[0]["status"] == "FAILED"
    assert "property" in (docs[0].get("processing_error") or "").lower()


# --- 5. Finalize discards uploads + audit ---


def test_07_finalize_discards_uploaded_files_and_writes_audit(client: TestClient, monkeypatch):
    mock_text(monkeypatch, SALE_DEED)
    headers = auth_header(client, "discard_user")
    case_id = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "VACANT_LAND"},
        headers=headers,
    ).json()["id"]
    doc_id = client.post(
        f"/property-cases/{case_id}/documents",
        files={"file": ("SaleDeed.pdf", io.BytesIO(tiny_pdf()), "application/pdf")},
        headers=headers,
    ).json()["id"]
    client.post(f"/property-cases/{case_id}/documents/{doc_id}/analyze", headers=headers)

    db = client.session_factory()
    try:
        document = db.get(Document, __import__("uuid").UUID(doc_id))
        path = Path(document.file_path)
        assert path.exists()
    finally:
        db.close()

    finalized = client.post(f"/property-cases/{case_id}/finalize", headers=headers)
    assert finalized.status_code == 200

    db = client.session_factory()
    try:
        document = db.get(Document, __import__("uuid").UUID(doc_id))
        assert document.status == DOCUMENT_STATUS_DISCARDED
        assert document.original_text is None
        assert document.extracted_data is not None
        assert document.file_path == ""
        assert not path.exists()
        actions = {row.action for row in db.scalars(select(AuditLog)).all()}
        assert "REPORT_FINALIZED" in actions
        assert "DOCUMENTS_DISCARDED" in actions
    finally:
        db.close()

    # Recalculate / second finalize still works from retained extracted_data
    again = client.post(f"/property-cases/{case_id}/finalize", headers=headers)
    assert again.status_code == 200
    assert again.json()["version"] == 2


# --- 6. RBAC: PDF + role assign + super admin ---


def test_08_buyer_cannot_download_pdf_secondary_admin_can(client: TestClient, monkeypatch):
    mock_text(monkeypatch, SALE_DEED)
    buyer = auth_header(client, "pdf_buyer")
    case_id = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "RESIDENTIAL_PLOT"},
        headers=buyer,
    ).json()["id"]
    doc_id = client.post(
        f"/property-cases/{case_id}/documents",
        files={"file": ("SaleDeed.pdf", io.BytesIO(tiny_pdf()), "application/pdf")},
        headers=buyer,
    ).json()["id"]
    client.post(f"/property-cases/{case_id}/documents/{doc_id}/analyze", headers=buyer)
    report = client.post(f"/property-cases/{case_id}/finalize", headers=buyer).json()

    denied = client.get(f"/property-cases/{case_id}/reports/{report['id']}/pdf", headers=buyer)
    assert denied.status_code == 403

    auth_header(client, "sec_admin")
    set_role(client, "sec_admin", ROLE_SECONDARY_ADMIN)
    staff = relogin(client, "sec_admin")
    allowed = client.get(f"/property-cases/{case_id}/reports/{report['id']}/pdf", headers=staff)
    assert allowed.status_code == 200
    assert allowed.headers["content-type"].startswith("application/pdf")


def test_09_super_admin_assigns_roles_and_lists_audit(client: TestClient):
    auth_header(client, "super")
    set_role(client, "super", ROLE_SUPER_ADMIN)
    super_headers = relogin(client, "super")

    target = signup(client, "to_promote").json()
    patched = client.patch(
        f"/admin/users/{target['id']}/role",
        json={"role": ROLE_ADMIN},
        headers=super_headers,
    )
    assert patched.status_code == 200
    assert patched.json()["role"] == ROLE_ADMIN

    logs = client.get("/admin/audit-logs", headers=super_headers)
    assert logs.status_code == 200
    assert any(item["action"] == "ROLE_ASSIGNED" for item in logs.json())

    buyer = auth_header(client, "plain_buyer")
    assert client.get("/admin/audit-logs", headers=buyer).status_code == 403


def test_10_staff_can_open_other_users_cases(client: TestClient):
    owner = auth_header(client, "case_owner")
    case_id = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "APARTMENT_FLAT"},
        headers=owner,
    ).json()["id"]
    auth_header(client, "admin1")
    set_role(client, "admin1", ROLE_ADMIN)
    admin = relogin(client, "admin1")
    assert client.get(f"/property-cases/{case_id}", headers=admin).status_code == 200


# --- 7. F1 / statistical scores on labelled fixtures ---


def test_11_binary_f1_and_accuracy_on_rule_fixtures():
    # Gold: litigation risk present / absent vs rule predictions on fixtures
    y_true = [True, True, False, False, True, False]
    y_pred = [True, False, False, True, True, False]
    scores = binary_scores(y_true, y_pred)
    assert scores["support"] == 6
    assert scores["true_positive"] == 2
    assert scores["false_positive"] == 1
    assert scores["false_negative"] == 1
    assert scores["true_negative"] == 2
    assert scores["precision"] == pytest.approx(2 / 3, rel=1e-3)
    assert scores["recall"] == pytest.approx(2 / 3, rel=1e-3)
    assert scores["f1"] == pytest.approx(2 / 3, rel=1e-3)
    assert scores["accuracy"] == pytest.approx(4 / 6, rel=1e-3)
    assert "statistical" in scores["note"].lower()
