from app.agents.base import FitnessAgent


class PersonalTrainerAgent(FitnessAgent):
    def __init__(self):
        super().__init__("personal_trainer")

    def default_prompt(self) -> str:
        return (
            "Você é um Personal Trainer especializado em esportes de endurance (ciclismo, corrida, natação, triathlon). "
            "Analise dados de treino do atleta e forneça:\n\n"
            "1. Análise de carga de treino (CTL, ATL, TSB) - tendências e recomendações\n"
            "2. Distribuição nas zonas de FC e potência\n"
            "3. Sugestões de treino para a próxima semana\n"
            "4. Identificação de pontos fortes e áreas de melhoria\n"
            "5. Risco de overtraining baseado nas tendências\n\n"
            "Formato da resposta:\n"
            "- Seja direto e objetivo\n"
            "- Use português brasileiro\n"
            "- Inclua métricas numéricas quando disponíveis\n"
            "- Sempre contextualize os números com recomendações práticas\n"
            "- Ao sugerir treinos, inclua: duração, zona de intensidade, e objetivo do treino"
        )

    async def create_workout_event(self, workout_data: dict) -> dict:
        return await self.intervals.create_event(workout_data)

    async def suggest_weekly_plan(self) -> str:
        system_prompt = (
            f"{self.default_prompt()}\n\n"
            "Gere um plano de treino semanal detalhado com dia a dia, "
            "incluindo tipo de treino, duração, zonas de intensidade, "
            "e objetivos de cada sessão. Formate como uma tabela."
        )
        activities = await self.get_recent_activities(days=14)
        wellness = await self.get_recent_wellness(days=7)
        fitness = await self.get_fitness_data(days=90)

        context = (
            f"DADOS DO ATLETA:\n\n"
            f"=== ATIVIDADES (14 dias) ===\n{activities}\n\n"
            f"=== WELLNESS (7 dias) ===\n{wellness}\n\n"
            f"=== FITNESS (90 dias) ===\n{fitness}\n\n"
            "Com base nesses dados, crie um plano semanal otimizado."
        )
        return await self.llm.chat(
            messages=[{"role": "user", "content": context}],
            system_prompt=system_prompt,
        )
