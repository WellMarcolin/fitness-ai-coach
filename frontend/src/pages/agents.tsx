import AgentConfig from '@/components/AgentConfig'

const agents = [
  {
    agentType: 'personal_trainer',
    title: 'Personal Trainer',
    icon: '🏋️',
    description: 'Análise de carga de treino, planos semanais, periodização e zonas de intensidade.',
  },
  {
    agentType: 'nutritionist',
    title: 'Nutricionista Esportivo',
    icon: '🥗',
    description: 'Recomendações de macros, planejamento alimentar pré/pós treino e análise corporal.',
  },
  {
    agentType: 'metabolism',
    title: 'Especialista em Metabolismo',
    icon: '🔄',
    description: 'Análise de HRV, recuperação, zonas metabólicas e risco de overtraining.',
  },
]

export default function AgentsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">Agentes de IA</h1>
      <p className="text-gray-500 mb-6 text-sm">
        Configure os prompts de sistema de cada agente. Eles definem o comportamento e especialidade de cada assistente.
      </p>
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <AgentConfig key={agent.agentType} {...agent} />
        ))}
      </div>
    </div>
  )
}
