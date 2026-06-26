import asyncio
import os
import pytest
from backend.auth import authenticate_user, create_access_token, get_current_user


def test_authenticate_user_success(monkeypatch):
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")
    user = authenticate_user("admin", "password")
    assert user is not False
    assert user["username"] == "admin"


def test_authenticate_user_failure(monkeypatch):
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")
    assert authenticate_user("admin", "wrong") is False


def test_create_access_token():
    token = create_access_token({"sub": "admin"})
    assert isinstance(token, str)


def test_get_current_user_success(monkeypatch):
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")
    token = create_access_token({"sub": "admin"})
    user = asyncio.run(get_current_user(token=token))
    assert user["username"] == "admin"


def test_get_current_user_invalid_token(monkeypatch):
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")
    with pytest.raises(Exception):
        asyncio.run(get_current_user(token="invalidtoken"))
