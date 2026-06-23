from fastapi import APIRouter, HTTPException
from typing import Literal

from app.models.schemas import (
    AgentType,
    AgentChatRequest,
    AgentChatResponse,
    AgentPromptConfig,
    AgentPromptResponse,
    AgentAnalyzeRequest,
    AgentGenerateRequest,
)
from app.agents.personal_trainer import PersonalTrainerAgent
from app.agents.nutritionist import NutritionistAgent
from app.agents.metabolism import MetabolismAgent

router = APIRouter()


def _get_agent(agent_type: AgentType):
    if agent_type == "personal_trainer":
        return PersonalTrainerAgent()
    elif agent_type == "nutritionist":
        return NutritionistAgent()
    elif agent_type == "metabolism":
        return MetabolismAgent()
    raise ValueError(f"Unknown agent: {agent_type}")


@router.post("/{agent_type}/chat")
async def agent_chat(agent_type: AgentType, request: AgentChatRequest):
    try:
        agent = _get_agent(agent_type)
        response = await agent.chat(request.message)

        chart_urls = []
        if request.include_charts:
            pass

        await agent.cleanup()
        return AgentChatResponse(
            agent_type=agent_type,
            response=response,
            chart_urls=chart_urls,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/analyze")
async def agent_analyze(agent_type: AgentType, request: AgentAnalyzeRequest):
    try:
        agent = _get_agent(agent_type)
        response = await agent.analyze(days=request.days)
        await agent.cleanup()
        return {"agent_type": agent_type, "analysis": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/generate")
async def agent_generate(agent_type: AgentType, request: AgentGenerateRequest):
    try:
        agent = _get_agent(agent_type)
        response = await agent.generate_plan(goal=request.goal, context=request.context)
        await agent.cleanup()
        return {"agent_type": agent_type, "plan": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_type}/prompt")
async def get_agent_prompt(agent_type: AgentType):
    try:
        agent = _get_agent(agent_type)
        prompt = await agent.get_system_prompt()
        await agent.cleanup()
        return AgentPromptResponse(agent_type=agent_type, system_prompt=prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{agent_type}/prompt")
async def update_agent_prompt(agent_type: AgentType, config: AgentPromptConfig):
    try:
        agent = _get_agent(agent_type)
        await agent.save_system_prompt(config.system_prompt)
        await agent.cleanup()
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Agent-specific endpoints ===

@router.post("/personal_trainer/weekly-plan")
async def get_weekly_plan():
    try:
        agent = PersonalTrainerAgent()
        plan = await agent.suggest_weekly_plan()
        await agent.cleanup()
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personal_trainer/create-workout")
async def create_workout(workout_data: dict):
    try:
        agent = PersonalTrainerAgent()
        result = await agent.create_workout_event(workout_data)
        await agent.cleanup()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nutritionist/meal-plan")
async def get_meal_plan(workout_description: str = ""):
    try:
        agent = NutritionistAgent()
        plan = await agent.meal_plan_for_workout(workout_description)
        await agent.cleanup()
        return {"meal_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutritionist/body-composition")
async def analyze_body_comp():
    try:
        agent = NutritionistAgent()
        analysis = await agent.analyze_body_composition()
        await agent.cleanup()
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metabolism/recovery-score")
async def get_recovery_score():
    try:
        agent = MetabolismAgent()
        score = await agent.recovery_score()
        await agent.cleanup()
        return {"recovery_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metabolism/zones")
async def analyze_zones():
    try:
        agent = MetabolismAgent()
        analysis = await agent.metabolic_zone_analysis()
        await agent.cleanup()
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
