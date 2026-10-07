import io
import sys
from pathlib import Path

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


def signup(client: TestClient, username: str = "advocate", password: str = "securePass1") -> dict:
    return client.post(
        "/auth/signup",
        json={"username": username, "password": password, "confirm_password": password},
    )


def login(client: TestClient, username: str = "advocate", password: str = "securePass1") -> dict:
    return client.post("/auth/login", json={"username": username, "password": password})


def auth_header(client: TestClient, username: str = "advocate", password: str = "securePass1") -> dict[str, str]:
    signup(client, username, password)
    token = login(client, username, password).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def tiny_pdf() -> bytes:
    return b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def test_signup_success(client: TestClient):
    response = signup(client)
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "advocate"
    assert "id" in body
    assert "password" not in body
    assert "password_hash" not in body


def test_duplicate_signup(client: TestClient):
    signup(client)
    response = signup(client)
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists."


def test_signup_password_mismatch(client: TestClient):
    response = client.post(
        "/auth/signup",
        json={"username": "mismatch", "password": "securePass1", "confirm_password": "otherPass1"},
    )
    assert response.status_code == 422
    assert "match" in response.json()["detail"].lower()


def test_login_success(client: TestClient):
    signup(client)
    response = login(client)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_invalid_login(client: TestClient):
    signup(client)
    response = login(client, password="wrong-password")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password."


def test_protected_endpoint_requires_auth(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_protected_endpoint_with_token(client: TestClient):
    headers = auth_header(client)
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "advocate"


def test_property_case_creation(client: TestClient):
    headers = auth_header(client)
    response = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "APARTMENT_FLAT"},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["domain"] == "RESIDENTIAL"
    assert body["property_type"] == "APARTMENT_FLAT"
    assert body["status"] == "ACTIVE"
    assert body["document_count"] == 0


def test_property_case_rejects_non_residential(client: TestClient):
    headers = auth_header(client)
    response = client.post(
        "/property-cases",
        json={"domain": "COMMERCIAL", "property_type": "APARTMENT_FLAT"},
        headers=headers,
    )
    assert response.status_code == 400
    assert "subscription" in response.json()["detail"].lower()


def test_document_upload(client: TestClient):
    headers = auth_header(client)
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "VILLA"},
        headers=headers,
    ).json()
    files = {"file": ("SaleDeed.pdf", io.BytesIO(tiny_pdf()), "application/pdf")}
    response = client.post(f"/property-cases/{case['id']}/documents", files=files, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["original_filename"] == "SaleDeed.pdf"
    assert body["status"] == "UPLOADED"
    assert body["file_type"] == "application/pdf"

    listed = client.get(f"/property-cases/{case['id']}/documents", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_unauthorized_case_access(client: TestClient):
    owner_headers = auth_header(client, "owner", "securePass1")
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "VACANT_LAND"},
        headers=owner_headers,
    ).json()

    other_headers = auth_header(client, "intruder", "securePass1")
    response = client.get(f"/property-cases/{case['id']}", headers=other_headers)
    assert response.status_code == 403
    assert "cannot open" in response.json()["detail"].lower()

    files = {"file": ("SaleDeed.pdf", io.BytesIO(tiny_pdf()), "application/pdf")}
    upload = client.post(f"/property-cases/{case['id']}/documents", files=files, headers=other_headers)
    assert upload.status_code == 403


def test_missing_property_case(client: TestClient):
    headers = auth_header(client)
    response = client.get("/property-cases/11111111-1111-1111-1111-111111111111", headers=headers)
    assert response.status_code == 404


def test_unsupported_file(client: TestClient):
    headers = auth_header(client)
    case = client.post(
        "/property-cases",
        json={"domain": "RESIDENTIAL", "property_type": "RESIDENTIAL_PLOT"},
        headers=headers,
    ).json()
    files = {"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")}
    response = client.post(f"/property-cases/{case['id']}/documents", files=files, headers=headers)
    assert response.status_code == 400
    assert "pdf" in response.json()["detail"].lower()
