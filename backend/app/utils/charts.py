import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import io
import base64


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.write_image(buf, format="png", width=1200, height=600, scale=2)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def _fig_to_html(fig) -> str:
    return fig.to_html(include_plotlyjs="cdn", full_html=False)


def plot_training_load(activities: list[dict], days: int = 90) -> dict:
    df = pd.DataFrame(activities)
    if df.empty or "start_date_local" not in df.columns:
        return {"error": "No data available"}

    df["date"] = pd.to_datetime(df["start_date_local"]).dt.date
    df = df.sort_values("date")

    fig = go.Figure()

    if "icu_training_load" in df.columns:
        fig.add_trace(go.Bar(
            x=df["date"],
            y=df["icu_training_load"],
            name="Carga do Treino",
            marker_color="rgba(54, 162, 235, 0.6)",
        ))

    if all(c in df.columns for c in ["icu_ctl", "icu_atl", "icu_tsb"]):
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["icu_ctl"],
            name="CTL (Fitness)", line=dict(color="green", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["icu_atl"],
            name="ATL (Fadiga)", line=dict(color="red", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["icu_tsb"],
            name="TSB (Forma)", line=dict(color="blue", width=2, dash="dash"),
        ))

    fig.update_layout(
        title=f"Carga de Treino - Últimos {days} dias",
        xaxis_title="Data",
        yaxis_title="Carga",
        hovermode="x unified",
        template="plotly_white",
        height=400,
    )

    return {
        "chart_type": "training_load",
        "image_base64": _fig_to_base64(fig),
        "html": _fig_to_html(fig),
        "data": df.to_dict(orient="records"),
    }


def plot_hr_zones(activity_streams: dict, activity_name: str = "Atividade") -> dict:
    fig = go.Figure()

    if "heartrate" in activity_streams:
        hr_data = activity_streams["heartrate"]
        fig.add_trace(go.Scatter(
            y=hr_data,
            name="FC",
            line=dict(color="red", width=1),
            fill="tozeroy",
            fillcolor="rgba(255,0,0,0.1)",
        ))
        fig.update_layout(
            title=f"Frequência Cardíaca - {activity_name}",
            xaxis_title="Tempo (amostras)",
            yaxis_title="FC (bpm)",
            height=350,
        )

    fig.update_layout(template="plotly_white")

    return {
        "chart_type": "hr_zones",
        "image_base64": _fig_to_base64(fig),
        "html": _fig_to_html(fig),
    }


def plot_body_composition(wellness_data: list[dict]) -> dict:
    df = pd.DataFrame(wellness_data)
    if df.empty:
        return {"error": "No data available"}

    df["date"] = pd.to_datetime(df["id"])
    df = df.sort_values("date")

    fig = go.Figure()

    if "weight" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["weight"],
            name="Peso (kg)",
            mode="lines+markers",
            line=dict(color="blue", width=2),
        ))

    if "body_fat" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["body_fat"],
            name="Gordura Corporal (%)",
            mode="lines+markers",
            line=dict(color="orange", width=2),
            yaxis="y2",
        ))

    fig.update_layout(
        title="Composição Corporal",
        xaxis_title="Data",
        yaxis_title="Peso (kg)",
        yaxis2=dict(title="Body Fat (%)", overlaying="y", side="right"),
        hovermode="x unified",
        template="plotly_white",
        height=400,
    )

    return {
        "chart_type": "body_composition",
        "image_base64": _fig_to_base64(fig),
        "html": _fig_to_html(fig),
        "data": df.to_dict(orient="records"),
    }


def plot_comparative(
    period_a: list[dict],
    period_b: list[dict],
    label_a: str = "Período A",
    label_b: str = "Período B",
) -> dict:
    df_a = pd.DataFrame(period_a)
    df_b = pd.DataFrame(period_b)

    fig = go.Figure()

    if not df_a.empty and "icu_training_load" in df_a.columns:
        fig.add_trace(go.Box(
            y=df_a["icu_training_load"],
            name=label_a,
            marker_color="blue",
        ))

    if not df_b.empty and "icu_training_load" in df_b.columns:
        fig.add_trace(go.Box(
            y=df_b["icu_training_load"],
            name=label_b,
            marker_color="orange",
        ))

    fig.update_layout(
        title="Comparativo de Carga de Treino",
        yaxis_title="Carga",
        template="plotly_white",
        height=400,
    )

    return {
        "chart_type": "comparative",
        "image_base64": _fig_to_base64(fig),
        "html": _fig_to_html(fig),
    }


def plot_weekly_summary(activities: list[dict], wellness: list[dict]) -> dict:
    df_act = pd.DataFrame(activities)
    df_well = pd.DataFrame(wellness)

    fig = go.Figure()
    fig.update_layout(
        title="Resumo Semanal",
        template="plotly_white",
        height=500,
    )

    if not df_act.empty and "start_date_local" in df_act.columns:
        df_act["date"] = pd.to_datetime(df_act["start_date_local"]).dt.date
        daily_load = df_act.groupby("date")["icu_training_load"].sum().reset_index()
        fig.add_trace(go.Bar(
            x=daily_load["date"],
            y=daily_load["icu_training_load"],
            name="Carga Diária",
            marker_color="rgba(54, 162, 235, 0.7)",
        ))

    if not df_well.empty and "resting_hr" in df_well.columns:
        df_well["date"] = pd.to_datetime(df_well["id"])
        fig.add_trace(go.Scatter(
            x=df_well["date"],
            y=df_well["resting_hr"],
            name="FC Repouso",
            line=dict(color="red", width=2),
            yaxis="y2",
        ))

    fig.update_layout(
        yaxis2=dict(title="FC Repouso (bpm)", overlaying="y", side="right"),
    )

    return {
        "chart_type": "weekly_summary",
        "image_base64": _fig_to_base64(fig),
        "html": _fig_to_html(fig),
    }
