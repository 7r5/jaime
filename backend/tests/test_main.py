from backend.main import app


def test_app_root():
    assert app.title == "WhatsApp Assistant Bot"
