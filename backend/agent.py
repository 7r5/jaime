from datetime import datetime
from sqlmodel import select
from . import ai
from .database import get_session
from .models import Conversation, QuestionnaireResult

QUESTIONNAIRES = {
    "default": [
        {"key": "name", "question": "¿Cuál es tu nombre?"},
        {"key": "email", "question": "¿Cuál es tu email?"},
        {"key": "reason", "question": "¿Cuál es el motivo de tu consulta?"},
    ]
}

async def handle_message(phone_number: str, text: str):
    with get_session() as session:
        statement = select(Conversation).where(Conversation.phone_number == phone_number)
        conversation = session.exec(statement).first()
        if not conversation:
            conversation = Conversation(phone_number=phone_number, state="questionnaire", context="default|0")
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        state = conversation.state
        current_context = conversation.context or "default|0"
        questionnaire_name, step = current_context.split("|")
        step = int(step)
        questionnaire = QUESTIONNAIRES.get(questionnaire_name, QUESTIONNAIRES["default"])

        if state == "questionnaire":
            if step > 0 and text.lower() not in ["hola", "hi", "buenos días", "buenas"]:
                store_answer(phone_number, questionnaire_name, questionnaire[step - 1]["key"], text)

            if step >= len(questionnaire):
                conversation.state = "complete"
                session.add(conversation)
                session.commit()
                provider = ai.get_provider()
                messages = [
                    {"role": "system", "content": "Eres un asistente de secretaria que responde de forma breve."},
                    {"role": "user", "content": text},
                ]
                return await provider.chat(messages)

            question = questionnaire[step]["question"]
            conversation.context = f"{questionnaire_name}|{step + 1}"
            session.add(conversation)
            session.commit()
            return question

        provider = ai.get_provider()
        messages = [
            {"role": "system", "content": "Eres un asistente de secretaria que usa herramientas cuando es útil."},
            {"role": "user", "content": text},
        ]
        return await provider.chat(messages)

def store_answer(phone_number: str, questionnaire_name: str, key: str, value: str):
    with get_session() as session:
        statement = select(QuestionnaireResult).where(
            QuestionnaireResult.phone_number == phone_number,
            QuestionnaireResult.questionnaire_name == questionnaire_name,
        )
        result = session.exec(statement).first()
        if not result:
            result = QuestionnaireResult(
                phone_number=phone_number,
                questionnaire_name=questionnaire_name,
                answers={},
                created_at=datetime.utcnow().isoformat(),
            )
        answers = dict(result.answers or {})
        answers[key] = value
        result.answers = answers
        session.add(result)
        session.commit()
