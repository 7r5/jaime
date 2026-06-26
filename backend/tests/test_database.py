import os
from pathlib import Path
from backend.database import create_db_and_tables, get_engine


def test_create_db_and_tables(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    engine = get_engine()
    assert "sqlite" in str(engine.url)
    create_db_and_tables()
    assert db_file.exists()
