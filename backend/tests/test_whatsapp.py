import os
import pytest
from backend.whatsapp import get_whatsapp_token, get_whatsapp_phone_number_id, get_whatsapp_verify_token


def test_get_whatsapp_verify_token_default(monkeypatch):
    monkeypatch.delenv("WHATSAPP_VERIFY_TOKEN", raising=False)
    assert get_whatsapp_verify_token() == "test_verify_token"


def test_get_whatsapp_verify_token_env(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "verify123")
    assert get_whatsapp_verify_token() == "verify123"


def test_get_whatsapp_token_and_phone_number_id(monkeypatch):
    monkeypatch.setenv("WHATSAPP_TOKEN", "token123")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "111")
    assert get_whatsapp_token() == "token123"
    assert get_whatsapp_phone_number_id() == "111"


@pytest.mark.asyncio
async def test_send_whatsapp_message_missing_env(monkeypatch):
    monkeypatch.delenv("WHATSAPP_TOKEN", raising=False)
    monkeypatch.delenv("WHATSAPP_PHONE_NUMBER_ID", raising=False)
    from backend.whatsapp import send_whatsapp_message
    with pytest.raises(RuntimeError):
        await send_whatsapp_message("1234", "hello")
