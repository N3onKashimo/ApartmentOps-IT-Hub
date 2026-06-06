from datetime import datetime
from pathlib import Path
import os
import uuid

import pandas as pd
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ApartmentOps Alert Bridge")

DATA_FILE = Path(os.getenv("TICKET_DATA_FILE", "../streamlit-hub/data/requests.csv"))

COLUMNS = [
    "ticket_id",
    "created_at",
    "source",
    "status",
    "priority",
    "service_name",
    "summary",
    "description",
    "raw_alert",
    "ai_summary",
    "kb_article",
]


def ensure_data_file():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)


def load_tickets():
    ensure_data_file()
    return pd.read_csv(DATA_FILE)


def save_tickets(df):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_FILE, index=False)


def create_ticket(payload: dict):
    df = load_tickets()

    service_name = (
        payload.get("monitor", {}).get("name")
        or payload.get("service_name")
        or payload.get("name")
        or "Unknown Service"
    )

    now = datetime.now().isoformat(timespec="seconds")

    ticket = {
        "ticket_id": f"INC-{uuid.uuid4().hex[:6].upper()}",
        "created_at": now,
        "source": "Uptime Kuma Webhook",
        "status": "Open",
        "priority": "Medium",
        "service_name": service_name,
        "summary": f"{service_name} generated an alert",
        "description": "Automated incident created from monitoring webhook.",
        "raw_alert": str(payload),
        "ai_summary": "AI summary placeholder. Connect NVIDIA API in nvidia_summary.py.",
        "kb_article": "KB-001 Service Unavailable Triage",
    }

    df = pd.concat([df, pd.DataFrame([ticket])], ignore_index=True)
    save_tickets(df)

    return ticket


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhook/uptime-kuma")
async def uptime_kuma_webhook(request: Request):
    payload = await request.json()
    ticket = create_ticket(payload)
    return {"created": True, "ticket": ticket}
