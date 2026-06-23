from app.agents.base import FitnessAgent


class NutritionistAgent(FitnessAgent):
    def __init__(self):
        super().__init__("nutritionist")

    def default_prompt(self) -> str:
        return (
            "Você é um Nutricionista Esportivo especializado em atletas de endurance. "
            "Analise os dados de treino, composição corporal e bem-estar do atleta e forneça:\n\n"
            "1. Cálculo de gasto calórico diário baseado nos treinos\n"
            "2. Recomendação de macronutrientes (g/kg de peso) para dias de treino e descanso\n"
            "3. Sugestões de refeições pré-treino, intra-treino e pós-treino\n"
            "4. Análise da evolução do peso e composição corporal\n"
            "5. Ajustes sazonais (off-season, pré-competição, competição)\n\n"
            "Formato da resposta:\n"
            "- Use português brasileiro\n"
            "- Seja prático e acionável\n"
            "- Inclua exemplos de alimentos e refeições\n"
            "- Considere horários dos treinos ao sugerir timing nutricional\n"
            "- Dê opções variadas (não repetir os mesmos alimentos todos os dias)"
        )

    async def analyze_body_composition(self) -> str:
        wellness = await self.get_recent_wellness(days=90)
        prompt = (
            "Analise a evolução da composição corporal (peso, body fat) nos últimos 90 dias. "
            "Identifique tendências, correlacione com períodos de treino e sugira ajustes nutricionais."
        )
        return await self.chat(prompt, context_data=f"Dados de wellness:\n{wellness}")

    async def meal_plan_for_workout(self, workout_description: str) -> str:
        prompt = (
            f"O atleta vai realizar o seguinte treino: {workout_description}\n\n"
            "Sugira o plano nutricional ideal para este treino específico, incluindo:\n"
            "- Refeição pré-treino (2-3h antes)\n"
            "- Snack pré-treino (30-60min antes)\n"
            "- Nutrição intra-treino\n"
            "- Refeição pós-treino (recuperação)\n"
            "- Hidratação"
        )
        return await self.chat(prompt)
