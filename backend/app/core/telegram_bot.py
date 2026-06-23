import logging
from datetime import datetime, date, timedelta
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from app.config import settings
from app.core.intervals_client import IntervalsClient
from app.agents.personal_trainer import PersonalTrainerAgent
from app.agents.nutritionist import NutritionistAgent
from app.agents.metabolism import MetabolismAgent
from app.utils.charts import (
    plot_training_load,
    plot_weekly_summary,
    plot_body_composition,
)

logger = logging.getLogger(__name__)

# Track user contexts (simple in-memory for MVP)
user_agents: dict = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏋️ **Fitness AI Coach**\n\n"
        "Eu sou seu assistente pessoal de treinamento, nutrição e metabolismo.\n\n"
        "**Comandos disponíveis:**\n"
        "/insights - Análise geral dos últimos 7 dias\n"
        "/treino - Gerar treino para hoje\n"
        "/nutricao - Sugestão nutricional\n"
        "/recuperacao - Análise de recuperação\n"
        "/grafico carga - Gráfico de carga de treino\n"
        "/grafico composicao - Gráfico de composição corporal\n"
        "/agente personal_trainer <msg> - Falar com Personal Trainer\n"
        "/agente nutritionist <msg> - Falar com Nutricionista\n"
        "/agente metabolism <msg> - Falar com Especialista em Metabolismo\n"
        "/config - Link para o dashboard web\n\n"
        "Use /help para mais informações.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "**Ajuda - Fitness AI Coach**\n\n"
        "Este bot conecta ao **intervals.icu** para acessar seus dados de treino, "
        "frequência cardíaca, sono, peso e composição corporal.\n\n"
        "**Agentes disponíveis:**\n"
        "• **Personal Trainer** - Análise de carga, planos de treino, periodização\n"
        "• **Nutricionista** - Macros, planejamento alimentar, timing nutricional\n"
        "• **Metabolismo** - HRV, recuperação, zonas metabólicas\n\n"
        "**Exemplos:**\n"
        "/insights - Resumo dos últimos 7 dias\n"
        "/treino - Treino recomendado para hoje\n"
        "/agente nutritionist \"O que comer antes de um pedal de 3h?\"\n\n"
        "Precisa configurar algo? Acesse o dashboard: "
        f"{settings.cors_origins.split(',')[0]}/settings",
        parse_mode="Markdown",
    )


async def insights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Analisando seus dados dos últimos 7 dias... ⏳")
    try:
        agent = PersonalTrainerAgent()
        analysis = await agent.analyze(days=7)
        await agent.cleanup()
        await update.message.reply_text(
            f"**📊 Análise dos Últimos 7 Dias**\n\n{analysis}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"Erro ao analisar dados: {str(e)}")


async def workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gerando treino para hoje... ⏳")
    try:
        agent = PersonalTrainerAgent()
        plan = await agent.suggest_weekly_plan()
        await agent.cleanup()
        await update.message.reply_text(
            f"**🏋️ Plano de Treino**\n\n{plan}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar treino: {str(e)}")


async def nutrition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Analisando dados nutricionais... ⏳")
    try:
        agent = NutritionistAgent()
        analysis = await agent.analyze(days=7)
        await agent.cleanup()
        await update.message.reply_text(
            f"**🥗 Recomendações Nutricionais**\n\n{analysis}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")


async def recovery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Calculando score de recuperação... ⏳")
    try:
        agent = MetabolismAgent()
        score = await agent.recovery_score()
        await agent.cleanup()
        await update.message.reply_text(
            f"**🔄 Análise de Recuperação**\n\n{score}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")


async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chart_type = args[0] if args else "carga"

    client = IntervalsClient()
    try:
        if chart_type in ("carga", "training_load", "load"):
            activities = await client.get_activities(
                oldest=date.today() - timedelta(days=90),
                newest=date.today(),
            )
            chart = plot_training_load(activities)
            if "image_base64" in chart:
                import base64
                from telegram import InputFile
                import io

                img_bytes = base64.b64decode(chart["image_base64"])
                await update.message.reply_photo(
                    photo=InputFile(io.BytesIO(img_bytes), filename="training_load.png"),
                    caption="📈 Carga de Treino - Últimos 90 dias",
                )
            else:
                await update.message.reply_text("Sem dados suficientes para gerar o gráfico.")

        elif chart_type in ("composicao", "body", "composition", "peso"):
            wellness = await client.get_wellness(
                oldest=date.today() - timedelta(days=90),
                newest=date.today(),
            )
            chart = plot_body_composition(wellness)
            if "image_base64" in chart:
                import base64
                from telegram import InputFile
                import io

                img_bytes = base64.b64decode(chart["image_base64"])
                await update.message.reply_photo(
                    photo=InputFile(io.BytesIO(img_bytes), filename="body_comp.png"),
                    caption="📊 Composição Corporal - Últimos 90 dias",
                )
            else:
                await update.message.reply_text("Sem dados suficientes.")
        else:
            await update.message.reply_text(
                "Tipos de gráfico: `carga`, `composicao`\n"
                "Exemplo: /grafico carga"
            )
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar gráfico: {str(e)}")
    finally:
        await client.close()


async def agent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Use: /agente <tipo> <mensagem>\n"
            "Tipos: personal_trainer, nutritionist, metabolism\n"
            "Exemplo: /agente personal_trainer Como está minha carga de treino?"
        )
        return

    agent_type = context.args[0]
    message = " ".join(context.args[1:])

    valid_types = {"personal_trainer", "nutritionist", "metabolism"}
    if agent_type not in valid_types:
        await update.message.reply_text(
            f"Tipo inválido. Use: {', '.join(valid_types)}"
        )
        return

    await update.message.reply_text(f"Consultando {agent_type}... ⏳")
    try:
        from app.api.agents import _get_agent
        agent = _get_agent(agent_type)
        response = await agent.chat(message)
        await agent.cleanup()
        await update.message.reply_text(
            f"**{agent_type.replace('_', ' ').title()}**\n\n{response}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base_url = settings.cors_origins.split(",")[0] if settings.cors_origins else "http://localhost:3000"
    keyboard = [
        [InlineKeyboardButton("Abrir Dashboard", url=f"{base_url}")],
        [InlineKeyboardButton("Configurações", url=f"{base_url}/settings")],
        [InlineKeyboardButton("Agentes", url=f"{base_url}/agents")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Configure seus agentes e conexões no dashboard:",
        reply_markup=reply_markup,
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


def create_application() -> Application:
    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("insights", insights))
    app.add_handler(CommandHandler("treino", workout))
    app.add_handler(CommandHandler("nutricao", nutrition))
    app.add_handler(CommandHandler("recuperacao", recovery))
    app.add_handler(CommandHandler("grafico", chart_command))
    app.add_handler(CommandHandler("agente", agent_command))
    app.add_handler(CommandHandler("config", config))
    app.add_error_handler(error_handler)

    return app


application = create_application()
