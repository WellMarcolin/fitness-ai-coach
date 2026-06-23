# Fitness AI Coach

## Visão Geral
Sistema com 3 agentes de IA (Personal Trainer, Nutricionista Esportivo, Especialista em Metabolismo) conectado ao **intervals.icu**, com interface via **Telegram Bot** e painel web **Next.js** para configuração e dashboards.

## Stack
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **LLM:** Multi-provedor (DeepSeek, GLM, Groq, Ollama) — configurável
- **Intervals.icu API:** `py-intervalsicu` + chamadas diretas REST
- **Telegram:** `python-telegram-bot` v20+ com webhooks
- **Gráficos:** Plotly (export PNG para Telegram) + Recharts (frontend)
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Banco Cache:** SQLite (dev) / PostgreSQL (opcional prod)
- **Deploy:** Docker Compose

## Estrutura do Projeto
```
fitness-ai-coach/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── config.py                # Settings (pydantic-settings)
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py            # Router principal /api/v1
│   │   │   ├── intervals.py         # Proxy endpoints intervals.icu
│   │   │   ├── agents.py            # Endpoints dos agentes IA
│   │   │   └── telegram.py          # Webhook do Telegram
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── intervals_client.py  # Cliente HTTP async para intervals.icu
│   │   │   ├── telegram_bot.py      # Lógica do bot Telegram
│   │   │   ├── llm.py               # Fábrica de providers LLM
│   │   │   ├── database.py          # SQLAlchemy async + models
│   │   │   └── llm_providers/
│   │   │       ├── __init__.py
│   │   │       ├── deepseek.py      # DeepSeek API (compatível OpenAI)
│   │   │       ├── glm.py           # GLM-4-Flash (Zhipu)
│   │   │       ├── groq.py          # Groq (Llama 3, Mixtral)
│   │   │       └── ollama.py        # Ollama local
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Classe base FitnessAgent
│   │   │   ├── personal_trainer.py # Skill: Personal Trainer
│   │   │   ├── nutritionist.py     # Skill: Nutricionista Esportivo
│   │   │   └── metabolism.py      # Skill: Metabolismo Esportivo
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py         # Pydantic models
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── charts.py          # Gráficos Plotly
│   │       └── analytics.py       # Análise de dados
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index.tsx          # Dashboard
│   │   │   ├── settings.tsx       # Configurações APIs
│   │   │   └── agents.tsx         # Configuração agentes
│   │   └── components/
│   │       ├── Charts/
│   │       │   ├── TrainingLoadChart.tsx
│   │       │   ├── HRZonesChart.tsx
│   │       │   └── BodyCompositionChart.tsx
│   │       ├── Layout.tsx
│   │       ├── AgentConfig.tsx
│   │       └── ApiConfig.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── PROJECT_OVERVIEW.md
```

## Agentes

### Personal Trainer
- Analisa carga de treino (CTL/ATL/TSB)
- Cria treinos estruturados no calendário intervals.icu
- Periodização e planos semanais
- Análise de zonas de FC e potência

### Nutricionista Esportivo
- Recomenda macros baseado no gasto calórico
- Planeja refeições pré/pós treino
- Analisa composição corporal (peso/BF%)
- Sugere timing de nutrientes

### Metabolismo Esportivo
- Analisa FC, HRV, sono, recuperação
- Define zonas metabólicas
- Risco de overtraining
- Eficiência energética

## APIs Integradas
| Serviço | Finalidade | Autenticação |
|---------|-----------|--------------|
| intervals.icu | Dados de treino, wellness, calendário | API Key |
| DeepSeek | LLM principal (opção 1) | API Key |
| GLM (Zhipu) | LLM alternativa (opção 2) | API Key |
| Groq | LLM alternativa (opção 3) | API Key |
| Ollama | LLM local (opção 4) | Localhost |
| Telegram | Comunicação com usuário | Bot Token |

## Fluxo Principal
```
intervals.icu ← → FastAPI Backend ← → LLM Provider
                     ↕                      ↕
              Telegram Bot           Next.js Frontend
                     ↕                      ↕
                [Usuário]            [Configurações / Dashboard]
```

## Comandos do Telegram
- `/start` — Boas-vindas + menu
- `/insights` — Análise dos últimos 7 dias
- `/treino` — Gerar treino do dia
- `/nutricao` — Sugestão nutricional
- `/recuperacao` — Análise de recuperação
- `/grafico <tipo>` — Enviar gráfico (carga, fc, peso)
- `/agente <nome> <msg>` — Falar diretamente com um agente
- `/config` — Link para o dashboard web
