import os, json
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import set_key

from app.config import settings as app_settings, _find_env, reload_settings

router = APIRouter()
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "settings.json")

# Map settings.json camelCase keys -> .env UPPER_CASE keys
SETTINGS_TO_ENV = {
    "intervalsAthleteId": "INTERVALS_ATHLETE_ID",
    "intervalsApiKey": "INTERVALS_API_KEY",
    "llmProvider": "LLM_PROVIDER",
    "deepseekApiKey": "DEEPSEEK_API_KEY",
    "glmApiKey": "GLM_API_KEY",
    "groqApiKey": "GROQ_API_KEY",
    "openrouterApiKey": "OPENROUTER_API_KEY",
    "opencodeApiKey": "OPENCODE_API_KEY",
    "telegramBotToken": "TELEGRAM_BOT_TOKEN",
}

SENSITIVE_KEYS = {
    "intervalsApiKey", "deepseekApiKey", "glmApiKey",
    "groqApiKey", "openrouterApiKey", "opencodeApiKey", "telegramBotToken",
}

MASK = "****"


def _mask(v: str) -> str:
    if len(v) <= 8:
        return MASK
    return v[:4] + MASK + v[-4:]


def _is_masked(v: str) -> bool:
    return MASK in v


def _load():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _sync_to_env(data: dict):
    env_path = _find_env()
    if not env_path:
        return

    for s_key, env_key in SETTINGS_TO_ENV.items():
        if s_key not in data:
            continue
        value = data[s_key]
        if _is_masked(value):
            continue
        set_key(env_path, env_key, value)
        attr = env_key.lower()
        if hasattr(app_settings, attr):
            setattr(app_settings, attr, value)


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


@router.get("/settings")
async def get_settings():
    data = _load()
    return {
        k: (_mask(v) if k in SENSITIVE_KEYS and v else v)
        for k, v in data.items()
    }


@router.put("/settings")
async def save_settings(data: SettingsData):
    payload = data.model_dump()
    _save(payload)
    _sync_to_env(payload)
    return {"status": "ok"}
