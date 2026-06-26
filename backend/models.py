from typing import Any, Optional
from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import SQLModel, Field

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    state: str = "new"
    context: Optional[str] = None

class QuestionnaireResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    questionnaire_name: str
    answers: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: str
