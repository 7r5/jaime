import os
import httpx
from .agent import handle_message


def get_whatsapp_verify_token() -> str:
    return os.getenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")


def get_whatsapp_token() -> str | None:
    return os.getenv("WHATSAPP_TOKEN")


def get_whatsapp_phone_number_id() -> str | None:
    return os.getenv("WHATSAPP_PHONE_NUMBER_ID")

async def process_whatsapp_event(payload: dict):
    entries = payload.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])
            for message in messages:
                from_number = message.get("from")
                text = message.get("text", {}).get("body")
                if from_number and text:
                    answer = await handle_message(from_number, text)
                    await send_whatsapp_message(from_number, answer)

async def send_whatsapp_message(to_number: str, text: str):
    token = get_whatsapp_token()
    phone_number_id = get_whatsapp_phone_number_id()
    if not token:
        raise RuntimeError("WHATSAPP_TOKEN no definido")
    if not phone_number_id:
        raise RuntimeError("WHATSAPP_PHONE_NUMBER_ID no definido")
    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, headers=headers)

def verify_whatsapp_signature() -> str:
    return get_whatsapp_verify_token()
