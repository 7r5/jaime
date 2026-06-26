from fastapi import APIRouter, Depends
from sqlmodel import select
from .auth import get_current_user
from .database import get_session
from .models import Conversation, QuestionnaireResult

router = APIRouter()

@router.get("/conversations")
async def list_conversations(current_user: dict = Depends(get_current_user)):
    with get_session() as session:
        statement = select(Conversation)
        conversations = session.exec(statement).all()
        return conversations

@router.get("/results")
async def list_results(current_user: dict = Depends(get_current_user)):
    with get_session() as session:
        statement = select(QuestionnaireResult)
        results = session.exec(statement).all()
        return results
