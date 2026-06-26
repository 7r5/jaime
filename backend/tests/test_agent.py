import asyncio
import os
import pytest
from sqlmodel import select
import backend.agent as agent
from backend.database import create_db_and_tables, get_session
from backend.models import Conversation, QuestionnaireResult


@pytest.mark.asyncio
async def test_questionnaire_flow(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    create_db_and_tables()

    async def fake_chat(messages, tools=None):
        return "Respuesta IA"

    monkeypatch.setattr(agent.ai, "get_provider", lambda: type("P", (), {"chat": fake_chat})())

    answer1 = await agent.handle_message("1234", "Hola")
    assert answer1 == "¿Cuál es tu nombre?"
    answer2 = await agent.handle_message("1234", "Juan")
    assert answer2 == "¿Cuál es tu email?"
    answer3 = await agent.handle_message("1234", "juan@example.com")
    assert answer3 == "¿Cuál es el motivo de tu consulta?"
    answer4 = await agent.handle_message("1234", "Consulta")
    assert answer4 == "Respuesta IA"

    from sqlmodel import select

    with get_session() as session:
        result = session.exec(
            select(QuestionnaireResult).where(QuestionnaireResult.phone_number == "1234")
        ).first()
        assert result is not None
        assert result.answers["name"] == "Juan"
        assert result.answers["email"] == "juan@example.com"
        assert result.answers["reason"] == "Consulta"


@pytest.mark.asyncio
async def test_handle_message_after_complete(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    create_db_and_tables()

    with get_session() as session:
        conversation = Conversation(phone_number="1234", state="complete", context="default|0")
        session.add(conversation)
        session.commit()

    async def fake_chat(messages, tools=None):
        return "Respuesta AI"

    monkeypatch.setattr(agent.ai, "get_provider", lambda: type("P", (), {"chat": fake_chat})())

    answer = await agent.handle_message("1234", "Hola")
    assert answer == "Respuesta AI"
