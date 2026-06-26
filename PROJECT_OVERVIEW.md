# Fitness AI Coach

## Visão Geral
Sistema com 3 agentes de IA (Personal Trainer, Nutricionista Esportivo, Especialista em Metabolismo) conectado ao **intervals.icu**, com interface via **Telegram Bot** e painel web **Next.js** para configuração e dashboards.

## Stack
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **LLM:** Multi-provedor (DeepSeek, GLM, Groq, Ollama, OpenRouter, OpenCode) — configurável
- **Intervals.icu API:** Cliente HTTP async custom (`httpx`) + REST direta
- **Telegram:** `python-telegram-bot` v20+ com webhooks (polling em dev)
- **Gráficos:** Plotly + Kaleido (export PNG para Telegram) + Recharts (frontend)
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, React Query, Axios
- **ORM Cache:** SQLAlchemy async + SQLite (dev) / PostgreSQL (opcional)
- **Deploy:** Docker Compose

## Estrutura do Projeto
```
fitness-ai-coach/
├── backend/
│   ├── run_bot.py                  # Entry point standalone do bot Telegram (polling)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── data/                       # Dados locais (SQLite, settings.json)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point + lifespan
│   │   ├── config.py               # Settings (pydantic-settings, .env)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py           # Router principal /api/v1
│   │   │   ├── intervals.py        # Proxy endpoints intervals.icu
│   │   │   ├── agents.py           # Endpoints dos agentes IA
│   │   │   ├── settings.py         # Endpoints de configuração (.env + settings.json)
│   │   │   └── telegram.py         # Webhook do Telegram
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # SQLAlchemy async + models de cache
│   │   │   ├── intervals_client.py # Cliente HTTP async para intervals.icu
│   │   │   ├── llm.py              # Fábrica abstrata de providers LLM
│   │   │   ├── telegram_bot.py     # Lógica do bot Telegram + handlers
│   │   │   └── llm_providers/
│   │   │       ├── __init__.py
│   │   │       ├── deepseek.py     # DeepSeek API (compatível OpenAI)
│   │   │       ├── glm.py          # GLM-4-Flash (Zhipu)
│   │   │       ├── groq.py         # Groq (Llama 3, Mixtral)
│   │   │       ├── ollama.py       # Ollama local
│   │   │       ├── openrouter.py   # OpenRouter (multi-modelo)
│   │   │       └── opencode.py     # OpenCode API
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Classe base FitnessAgent (LLM + Intervals)
│   │   │   ├── personal_trainer.py # Skill: Personal Trainer
│   │   │   ├── nutritionist.py     # Skill: Nutricionista Esportivo
│   │   │   └── metabolism.py       # Skill: Metabolismo Esportivo
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py          # Pydantic models (requests/responses)
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── charts.py           # Gráficos Plotly (PNG base64)
│   │       └── analytics.py        # Análise estatística de dados
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── src/
│   │   ├── styles/
│   │   │   └── globals.css         # Estilos globais Tailwind
│   │   ├── pages/
│   │   │   ├── _app.tsx            # Next.js App wrapper
│   │   │   ├── _document.tsx       # Next.js Document wrapper
│   │   │   ├── index.tsx           # Dashboard com métricas (CTL/ATL/TSB, FC, HRV, sono)
│   │   │   ├── settings.tsx        # Configurações de APIs
│   │   │   └── agents.tsx          # Configuração de prompts dos agentes
│   │   └── components/
│   │       ├── Layout.tsx
│   │       ├── AgentConfig.tsx     # Editor de system prompt por agente
│   │       ├── ApiConfig.tsx       # Formulário de credenciais
│   │       └── Charts/
│   │           ├── TrainingLoadChart.tsx
│   │           ├── HRZonesChart.tsx
│   │           └── BodyCompositionChart.tsx
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
- Sugere plano semanal via LLM

### Nutricionista Esportivo
- Recomenda macros baseado no gasto calórico
- Planeja refeições pré/pós treino
- Analisa composição corporal (peso/BF%)
- Sugere timing de nutrientes
- Gera plano alimentar para treinos específicos

### Metabolismo Esportivo
- Analisa FC, HRV, sono, recuperação
- Define zonas metabólicas
- Calcula score de recuperação (0-100)
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
| OpenRouter | LLM alternativa (opção 5) | API Key |
| OpenCode | LLM alternativa (opção 6) | API Key |
| Telegram | Comunicação com usuário | Bot Token |

## Fluxo Principal
```
intervals.icu ← → FastAPI Backend ← → LLM Provider (DeepSeek/GLM/Groq/Ollama/OpenRouter/OpenCode)
                     ↕                            ↕
              Telegram Bot                 Next.js Frontend
              (polling/webhook)          (Dashboard / Config)
                     ↕                            ↕
                [Usuário]              [Configurações / Dashboards]
```

## Comandos do Telegram
- `/start` — Boas-vindas + menu principal
- `/help` — Informações detalhadas e exemplos
- `/insights` — Análise dos últimos 7 dias
- `/treino` — Gerar plano de treino semanal
- `/nutricao` — Sugestão nutricional
- `/recuperacao` — Score de recuperação (0-100)
- `/grafico <tipo>` — Enviar gráfico (`carga`, `composicao`)
- `/agente <tipo> <msg>` — Falar diretamente com um agente (`personal_trainer`, `nutritionist`, `metabolism`)
- `/config` — Link para o dashboard web com botões inline
