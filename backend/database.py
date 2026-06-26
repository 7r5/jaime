import os
from sqlmodel import SQLModel, create_engine, Session


def get_engine():
    database_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    return create_engine(database_url, echo=False)


def create_db_and_tables():
    from .models import Conversation, QuestionnaireResult
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(get_engine())
