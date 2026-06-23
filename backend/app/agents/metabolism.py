from app.agents.base import FitnessAgent


class MetabolismAgent(FitnessAgent):
    def __init__(self):
        super().__init__("metabolism")

    def default_prompt(self) -> str:
        return (
            "Você é um Especialista em Metabolismo Esportivo e Fisiologia do Exercício. "
            "Analise dados de frequência cardíaca, HRV, sono, recuperação e desempenho para fornecer:\n\n"
            "1. Análise da variabilidade da frequência cardíaca (HRV) e sistema nervoso autônomo\n"
            "2. Qualidade da recuperação (sono, FC de repouso, HRV)\n"
            "3. Eficiência metabólica (custo energético do movimento, economia de corrida/pedalada)\n"
            "4. Identificação de zonas metabólicas e transições aeróbica/anaeróbica\n"
            "5. Risco de overtraining syndrome baseado em múltiplos marcadores\n"
            "6. Correlação entre qualidade do sono e desempenho nos treinos\n\n"
            "Formato da resposta:\n"
            "- Use português brasileiro\n"
            "- Baseie-se em evidências científicas (\u200ecite estudos quando relevante)\n"
            "- Dê scores/notas para cada marcador (ex: Recuperação: 7/10)\n"
            "- Priorize recomendações práticas baseadas nos dados\n"
            "- Identifique padrões ao longo do tempo, não apenas snapshots"
        )

    async def recovery_score(self) -> str:
        wellness = await self.get_recent_wellness(days=7)
        activities = await self.get_recent_activities(days=3)
        prompt = (
            "Calcule um score de recuperação (0-100) para hoje baseado nos dados dos últimos 7 dias. "
            "Considere: HRV, qualidade do sono, FC de repouso, fadiga reportada, "
            "e carga dos treinos recentes. Explique cada componente do score."
        )
        return await self.chat(prompt, context_data=f"Wellness:\n{wellness}\n\nAtividades:\n{activities}")

    async def metabolic_zone_analysis(self) -> str:
        activities = await self.get_recent_activities(days=30)
        prompt = (
            "Analise a distribuição do tempo do atleta nas zonas de FC e potência "
            "nos últimos 30 dias. Identifique:\n"
            "- Quanto tempo em zona aeróbica vs anaeróbica\n"
            "- Se o perfil está alinhado com os objetivos do atleta\n"
            "- Sugestões para otimizar o treinamento metabólico\n"
            "- Eficiência na transição entre zonas"
        )
        return await self.chat(prompt, context_data=f"Atividades:\n{activities}")
