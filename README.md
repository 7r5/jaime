# WhatsApp Assistant Bot

Proyecto de bot de WhatsApp con backend en Python/FastAPI, frontend en React y despliegue en Render.

## Arquitectura

- `backend/`: FastAPI, webhook de WhatsApp, lógica de agente, persistencia SQLite.
- `frontend/`: React app con login y dashboard.
- `render.yaml`: configuración para desplegar en Render.

## Flujo

1. WhatsApp envía mensajes a webhook.
2. Backend procesa el mensaje usando un agente IA.
3. El bot recolecta datos y guarda respuestas en la base de datos.
4. El frontend muestra los resultados y permite ver JSON.

## Variables de entorno

- `OPENAI_API_KEY` o `CLAUDE_API_KEY`
- `AI_PROVIDER` (openai | claude)
- `WHATSAPP_TOKEN`
- `WHATSAPP_VERIFY_TOKEN`
- `ADMIN_USER`
- `ADMIN_PASSWORD`
- `DATABASE_URL`
- `SECRET_KEY`

## Configuración de VS Code

Este proyecto usa `poetry` para gestionar dependencias. En VS Code, selecciona el intérprete Python que Poetry crea para el proyecto en `backend/`.

No es necesario forzar un path fijo dentro de `.vscode/settings.json`. Si deseas usar un entorno local creado por Poetry, la ruta típica en Windows sería `backend/.venv/Scripts/python.exe`, pero ese archivo de configuración debe ser local y no parte del repositorio.

Si usas la configuración global de Poetry y el entorno no se crea dentro del proyecto, selecciona el intérprete Python creado por Poetry desde la paleta de comandos.

## Instalación backend

```bash
cd backend
poetry install
```

Para ejecutar el backend:

```bash
cd backend
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Si prefieres activar el shell de Poetry:

```bash
cd backend
poetry shell
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

> Nota: el backend usa `pyproject.toml` / `poetry.lock` para dependencias. `requirements.txt` no es parte del flujo principal.


## Instalación frontend

```bash
cd frontend
npm install
```

## Despliegue en Render

- Usa el archivo `render.yaml`.
- Configura las variables de entorno en el panel de Render.
