from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response, JSONResponse
from .whatsapp import verify_whatsapp_signature, process_whatsapp_event

router = APIRouter()

@router.get("/")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == verify_whatsapp_signature():
        return Response(content=challenge or "", media_type="text/plain")
    raise HTTPException(status_code=400, detail="Invalid webhook verification")

@router.post("/")
async def receive_message(payload: dict):
    await process_whatsapp_event(payload)
    return JSONResponse(content={"status": "received"})
