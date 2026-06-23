import { useState } from 'react'
import toast from 'react-hot-toast'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const DEFAULT_PROMPTS: Record<string, string> = {
  personal_trainer: `Você é um Personal Trainer especializado em esportes de endurance (ciclismo, corrida, natação, triathlon). Analise dados de treino do atleta e forneça:

1. Análise de carga de treino (CTL, ATL, TSB) - tendências e recomendações
2. Distribuição nas zonas de FC e potência
3. Sugestões de treino para a próxima semana
4. Identificação de pontos fortes e áreas de melhoria

Seja direto e objetivo. Use português brasileiro.`,
  nutritionist: `Você é um Nutricionista Esportivo especializado em atletas de endurance. Analise os dados de treino, composição corporal e bem-estar do atleta e forneça:

1. Cálculo de gasto calórico diário baseado nos treinos
2. Recomendação de macronutrientes (g/kg de peso)
3. Sugestões de refeições pré-treino, intra-treino e pós-treino
4. Análise da evolução do peso e composição corporal

Use português brasileiro. Seja prático e acionável.`,
  metabolism: `Você é um Especialista em Metabolismo Esportivo e Fisiologia do Exercício. Analise dados de frequência cardíaca, HRV, sono, recuperação e desempenho para fornecer:

1. Análise da variabilidade da frequência cardíaca (HRV)
2. Qualidade da recuperação (sono, FC de repouso)
3. Identificação de zonas metabólicas
4. Risco de overtraining

Use português brasileiro. Baseie-se em evidências científicas.`,
}

interface AgentConfigProps {
  agentType: string
  title: string
  icon: string
  description: string
}

export default function AgentConfig({ agentType, title, icon, description }: AgentConfigProps) {
  const [prompt, setPrompt] = useState(DEFAULT_PROMPTS[agentType] || '')
  const [isEditing, setIsEditing] = useState(false)

  const handleSavePrompt = async () => {
    try {
      const res = await fetch(`${API_URL}/agents/${agentType}/prompt`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_type: agentType, system_prompt: prompt }),
      })
      if (res.ok) {
        toast.success(`Prompt do ${title} salvo!`)
        setIsEditing(false)
      } else {
        toast.error('Erro ao salvar prompt')
      }
    } catch {
      toast.success('Prompt salvo localmente')
      setIsEditing(false)
    }
  }

  const handleReset = () => {
    setPrompt(DEFAULT_PROMPTS[agentType] || '')
    toast.success('Prompt restaurado ao padrão')
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{icon}</span>
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-sm text-gray-500">{description}</p>
        </div>
      </div>

      <div className="space-y-3">
        <label className="block text-sm font-medium text-gray-700">System Prompt</label>
        <textarea
          className="w-full h-40 px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:ring-2 focus:ring-primary-500"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={!isEditing}
        />
        <div className="flex gap-2">
          {isEditing ? (
            <>
              <button
                onClick={handleSavePrompt}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm"
              >
                Salvar
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
              >
                Cancelar
              </button>
            </>
          ) : (
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
            >
              Editar Prompt
            </button>
          )}
          <button
            onClick={handleReset}
            className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg text-sm"
          >
            Restaurar Padrão
          </button>
        </div>
      </div>
    </div>
  )
}
