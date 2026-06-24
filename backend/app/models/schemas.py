from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date, datetime


# === Agent Types ===
AgentType = Literal["personal_trainer", "nutritionist", "metabolism"]


class AgentPromptConfig(BaseModel):
    agent_type: AgentType
    system_prompt: str


class AgentPromptResponse(BaseModel):
    agent_type: AgentType
    system_prompt: str


# === Intervals.icu ===
class IntervalSettings(BaseModel):
    athlete_id: str
    api_key: str


class ActivitySummary(BaseModel):
    id: str
    name: str
    start_date_local: datetime
    type: str
    distance: Optional[float] = None
    moving_time: Optional[float] = None
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    icu_training_load: Optional[float] = None
    icu_atl: Optional[float] = None
    icu_ctl: Optional[float] = None
    icu_tsb: Optional[float] = None
    average_watts: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    calories: Optional[float] = None


class WellnessRecord(BaseModel):
    id: str  # ISO date
    resting_hr: Optional[int] = None
    hrv: Optional[float] = None
    sleep_secs: Optional[int] = None
    sleep_score: Optional[float] = None
    fatigue: Optional[int] = None
    soreness: Optional[int] = None
    stress: Optional[int] = None
    mood: Optional[int] = None
    weight: Optional[float] = None
    body_fat: Optional[float] = None
    notes: Optional[str] = None


# === LLM Provider Settings ===
class LLMProviderSettings(BaseModel):
    provider: Literal["deepseek", "glm", "groq", "ollama", "openrouter", "opencode"]
    api_key: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None


# === Chat / Agent Requests ===
class AgentChatRequest(BaseModel):
    agent_type: AgentType
    message: str
    include_charts: bool = False


class AgentChatResponse(BaseModel):
    agent_type: AgentType
    response: str
    chart_urls: list[str] = []


class AgentAnalyzeRequest(BaseModel):
    agent_type: AgentType
    days: int = 7


class AgentGenerateRequest(BaseModel):
    agent_type: AgentType
    goal: str = ""
    context: str = ""


# === Workout ===
class WorkoutEvent(BaseModel):
    name: str
    description: str
    start_date_local: datetime
    category: str = "WORKOUT"
    sport: Optional[str] = None
    duration: Optional[int] = None


# === Charts ===
class ChartRequest(BaseModel):
    chart_type: Literal["training_load", "hr_zones", "body_composition", "comparative"]
    days: int = 30
    activity_id: Optional[str] = None


class ChartResponse(BaseModel):
    chart_type: str
    image_base64: Optional[str] = None
    data: Optional[dict] = None


# === Dashboard ===
class DashboardData(BaseModel):
    current_ctl: Optional[float] = None
    current_atl: Optional[float] = None
    current_tsb: Optional[float] = None
    resting_hr: Optional[int] = None
    hrv: Optional[float] = None
    sleep_avg: Optional[float] = None
    weekly_load: Optional[float] = None
    last_activity: Optional[ActivitySummary] = None
