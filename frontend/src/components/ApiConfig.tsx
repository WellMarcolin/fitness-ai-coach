import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function ApiConfig() {
  const [config, setConfig] = useState({
    intervalsAthleteId: '',
    intervalsApiKey: '',
    llmProvider: 'deepseek',
    deepseekApiKey: '',
    glmApiKey: '',
    groqApiKey: '',
    openrouterApiKey: '',
    opencodeApiKey: '',
    telegramBotToken: '',
  })

  useEffect(() => {
    fetch(`${API_URL}/settings`)
      .then(r => r.json())
      .then(data => {
        if (data && data.llmProvider) setConfig(data)
      })
      .catch(() => {})
  }, [])

  const handleSave = async () => {
    try {
      const res = await fetch(`${API_URL}/settings`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      })
      if (res.ok) {
        toast.success('Configurações salvas!')
      } else {
        toast.error('Erro ao salvar')
      }
    } catch {
      toast.error('Erro de conexão com o servidor')
    }
  }

  const handleTest = async (service: string) => {
    toast.loading(`Testando ${service}...`)

    if (service === 'intervals') {
      try {
        const res = await fetch(`${API_URL}/intervals/athlete`)
        if (res.ok) {
          toast.dismiss()
          toast.success('intervals.icu: Conexão OK!')
        } else {
          toast.dismiss()
          toast.error('intervals.icu: Falha na conexão')
        }
      } catch {
        toast.dismiss()
        toast.error('intervals.icu: Erro de conexão')
      }
    } else if (service === 'telegram') {
      try {
        const res = await fetch(`${API_URL}/telegram/info`)
        if (res.ok) {
          toast.dismiss()
          toast.success('Telegram: Conexão OK!')
        } else {
          toast.dismiss()
          toast.error('Telegram: Falha na conexão')
        }
      } catch {
        toast.dismiss()
        toast.error('Telegram: Erro de conexão')
      }
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold mb-4">intervals.icu</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Athlete ID</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="i123456"
              value={config.intervalsAthleteId}
              onChange={(e) => setConfig({ ...config, intervalsAthleteId: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
            <input
              type="password"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Sua API key"
              value={config.intervalsApiKey}
              onChange={(e) => setConfig({ ...config, intervalsApiKey: e.target.value })}
            />
          </div>
          <button
            onClick={() => handleTest('intervals')}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
          >
            Testar Conexão
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold mb-4">Provedor LLM</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              value={config.llmProvider}
              onChange={(e) => setConfig({ ...config, llmProvider: e.target.value })}
            >
              <option value="deepseek">DeepSeek</option>
              <option value="glm">GLM (Zhipu)</option>
              <option value="groq">Groq</option>
              <option value="ollama">Ollama (Local)</option>
              <option value="openrouter">OpenRouter</option>
              <option value="opencode">OpenCode API</option>
            </select>
          </div>
          {config.llmProvider !== 'ollama' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Key ({config.llmProvider})
              </label>
              <input
                type="password"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="API key"
                value={
                  config.llmProvider === 'deepseek' ? config.deepseekApiKey :
                  config.llmProvider === 'glm' ? config.glmApiKey :
                  config.llmProvider === 'groq' ? config.groqApiKey :
                  config.llmProvider === 'openrouter' ? config.openrouterApiKey :
                  config.opencodeApiKey
                }
                onChange={(e) => {
                  const key = e.target.value
                  if (config.llmProvider === 'deepseek') setConfig({ ...config, deepseekApiKey: key })
                  else if (config.llmProvider === 'glm') setConfig({ ...config, glmApiKey: key })
                  else if (config.llmProvider === 'groq') setConfig({ ...config, groqApiKey: key })
                  else if (config.llmProvider === 'openrouter') setConfig({ ...config, openrouterApiKey: key })
                  else setConfig({ ...config, opencodeApiKey: key })
                }}
              />
            </div>
          )}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold mb-4">Telegram Bot</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bot Token</label>
            <input
              type="password"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="Seu token do Telegram"
              value={config.telegramBotToken}
              onChange={(e) => setConfig({ ...config, telegramBotToken: e.target.value })}
            />
          </div>
          <button
            onClick={() => handleTest('telegram')}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm"
          >
            Testar Conexão
          </button>
        </div>
      </div>

      <button
        onClick={handleSave}
        className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium"
      >
        Salvar Configurações
      </button>
    </div>
  )
}
