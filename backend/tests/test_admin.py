import os
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import create_db_and_tables, get_session
from backend.models import Conversation, QuestionnaireResult


def setup_database(tmp_path):
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    create_db_and_tables()


def test_admin_endpoints_require_auth(monkeypatch, tmp_path):
    setup_database(tmp_path)
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")

    token = "wrong"
    client = TestClient(app)
    response = client.get("/admin/conversations", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_admin_endpoints_can_list_conversations(tmp_path, monkeypatch):
    setup_database(tmp_path)
    with get_session() as session:
        session.add(Conversation(phone_number="1234", state="questionnaire", context="default|0"))
        session.add(QuestionnaireResult(phone_number="1234", questionnaire_name="default", answers={"name": "Juan"}, created_at="2026-01-01T00:00:00"))
        session.commit()

    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")
    client = TestClient(app)
    response = client.post("/auth/token", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/admin/conversations", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
