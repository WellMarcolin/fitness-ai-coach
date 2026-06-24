from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional

from app.core.llm import LLMProvider, get_llm_provider
from app.core.intervals_client import IntervalsClient
from app.core.database import async_session, AgentPrompt


class FitnessAgent(ABC):
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self._llm: Optional[LLMProvider] = None
        self._intervals: Optional[IntervalsClient] = None
        self._system_prompt: Optional[str] = None

    @property
    def llm(self) -> LLMProvider:
        if self._llm is None:
            self._llm = get_llm_provider()
        return self._llm

    @property
    def intervals(self) -> IntervalsClient:
        if self._intervals is None:
            self._intervals = IntervalsClient()
        return self._intervals

    @abstractmethod
    def default_prompt(self) -> str:
        ...

    async def get_system_prompt(self) -> str:
        if self._system_prompt:
            return self._system_prompt
        async with async_session() as session:
            row = await session.get(AgentPrompt, self.agent_type)
            if row:
                self._system_prompt = row.system_prompt
                return row.system_prompt
        return self.default_prompt()

    async def save_system_prompt(self, prompt: str):
        self._system_prompt = prompt
        async with async_session() as session:
            row = await session.get(AgentPrompt, self.agent_type)
            if row:
                row.system_prompt = prompt
            else:
                session.add(AgentPrompt(agent_type=self.agent_type, system_prompt=prompt))
            await session.commit()

    async def get_recent_activities(self, days: int = 7) -> str:
        newest = date.today()
        oldest = newest - timedelta(days=days)
        data = await self.intervals.get_activities(oldest=oldest, newest=newest)
        import json
        return json.dumps(data, indent=2, default=str)

    async def get_recent_wellness(self, days: int = 7) -> str:
        newest = date.today()
        oldest = newest - timedelta(days=days)
        data = await self.intervals.get_wellness(oldest=oldest, newest=newest)
        import json
        return json.dumps(data, indent=2, default=str)

    async def get_fitness_data(self, days: int = 90) -> str:
        from datetime import timedelta
        newest = date.today()
        oldest = newest - timedelta(days=days)
        data = await self.intervals.get_activities(
            oldest=oldest, newest=newest,
            fields="id,name,start_date_local,icu_training_load,icu_atl,icu_ctl,icu_tsb"
        )
        import json
        return json.dumps(data, indent=2, default=str)

    async def analyze(self, days: int = 7) -> str:
        prompt = await self.get_system_prompt()
        activities = await self.get_recent_activities(days=days)
        wellness = await self.get_recent_wellness(days=days)
        fitness = await self.get_fitness_data(days=90)

        context = (
            f"DADOS DOS ÚLTIMOS {days} DIAS:\n\n"
            f"=== ATIVIDADES ===\n{activities}\n\n"
            f"=== WELLNESS ===\n{wellness}\n\n"
            f"=== FITNESS (CTL/ATL/TSB) ===\n{fitness}\n\n"
            "Com base nesses dados, forneça uma análise detalhada."
        )
        return await self.llm.chat(
            messages=[{"role": "user", "content": context}],
            system_prompt=prompt,
        )

    async def chat(self, message: str, context_data: Optional[str] = None) -> str:
        prompt = await self.get_system_prompt()
        if context_data:
            message = f"{context_data}\n\nPergunta do usuário: {message}"
        return await self.llm.chat(
            messages=[{"role": "user", "content": message}],
            system_prompt=prompt,
        )

    async def generate_plan(self, goal: str, context: str = "") -> str:
        prompt = await self.get_system_prompt()
        activities = await self.get_recent_activities(days=14)
        wellness = await self.get_recent_wellness(days=14)

        full_context = (
            f"DADOS DO ATLETA:\n\n"
            f"=== ATIVIDADES (14 dias) ===\n{activities}\n\n"
            f"=== WELLNESS (14 dias) ===\n{wellness}\n\n"
            f"Objetivo: {goal}\n"
            f"Contexto extra: {context}\n\n"
            "Com base nesses dados e seu conhecimento, gere um plano detalhado."
        )
        return await self.llm.chat(
            messages=[{"role": "user", "content": full_context}],
            system_prompt=prompt,
        )

    async def cleanup(self):
        if self._intervals:
            await self._intervals.close()
