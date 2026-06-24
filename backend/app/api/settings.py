from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json, os

router = APIRouter()
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "settings.json")

class SettingsData(BaseModel):
    intervalsAthleteId: str = ""
    intervalsApiKey: str = ""
    llmProvider: str = "deepseek"
    deepseekApiKey: str = ""
    glmApiKey: str = ""
    groqApiKey: str = ""
    openrouterApiKey: str = ""
    opencodeApiKey: str = ""
    telegramBotToken: str = ""

def _load():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return {}

def _save(data: dict):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.get("/settings")
async def get_settings():
    return _load()

@router.put("/settings")
async def save_settings(data: SettingsData):
    _save(data.model_dump())
    return {"status": "ok"}
