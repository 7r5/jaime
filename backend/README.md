# WhatsApp Assistant Backend

Backend de FastAPI para el bot de WhatsApp.

## Uso

```bash
cd backend
poetry install
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Opción con shell de Poetry:

```bash
cd backend
poetry shell
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Variables de entorno

- `OPENAI_API_KEY` o `CLAUDE_API_KEY`
- `AI_PROVIDER` (openai | claude)
- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_VERIFY_TOKEN`
- `ADMIN_USER`
- `ADMIN_PASSWORD`
- `DATABASE_URL`
- `SECRET_KEY`

> Nota: este backend gestiona dependencias con Poetry. Usa `pyproject.toml` y `poetry.lock` en lugar de `requirements.txt`.
