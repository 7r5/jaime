from fastapi.testclient import TestClient
import os
from backend.main import app
from backend.whatsapp import verify_whatsapp_signature
import backend.webhook as webhook_module


def test_verify_webhook_success(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")
    client = TestClient(app)
    response = client.get("/webhook/?hub.mode=subscribe&hub.verify_token=test_verify_token&hub.challenge=1234")
    assert response.status_code == 200
    assert response.text == "1234"


def test_verify_webhook_failure(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")
    client = TestClient(app)
    response = client.get("/webhook/?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=1234")
    assert response.status_code == 400


def test_verify_whatsapp_signature(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "verify123")
    assert verify_whatsapp_signature() == "verify123"


def test_receive_message_posts_event(monkeypatch):
    called = {"payload": None}

    async def fake_process(payload):
        called["payload"] = payload

    monkeypatch.setattr("backend.webhook.process_whatsapp_event", fake_process)
    client = TestClient(app)
    response = client.post("/webhook/", json={"entry": []})
    assert response.status_code == 200
    assert response.json() == {"status": "received"}
    assert called["payload"] == {"entry": []}
