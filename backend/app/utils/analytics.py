import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Optional


def calculate_weekly_load(activities: list[dict]) -> dict:
    df = pd.DataFrame(activities)
    if df.empty:
        return {"weekly_load": 0, "daily_avg": 0}

    if "start_date_local" in df.columns:
        df["date"] = pd.to_datetime(df["start_date_local"]).dt.date
        df["week"] = pd.to_datetime(df["start_date_local"]).dt.isocalendar().week

    weekly = {}
    if "icu_training_load" in df.columns:
        weekly_load = df.groupby("week")["icu_training_load"].sum()
        weekly = weekly_load.to_dict()

    return {
        "weekly_load": float(df["icu_training_load"].sum()) if "icu_training_load" in df.columns else 0,
        "daily_avg": float(df["icu_training_load"].mean()) if "icu_training_load" in df.columns else 0,
        "by_week": weekly,
    }


def calculate_recovery_score(wellness_data: list[dict]) -> dict:
    df = pd.DataFrame(wellness_data)
    if df.empty:
        return {"score": 50, "factors": {}}

    score = 100
    factors = {}

    if "hrv" in df.columns and not df["hrv"].isna().all():
        recent_hrv = df["hrv"].dropna().tail(7).mean()
        factors["hrv"] = float(recent_hrv) if not pd.isna(recent_hrv) else 0

    if "resting_hr" in df.columns and not df["resting_hr"].isna().all():
        recent_hr = df["resting_hr"].dropna().tail(3).mean()
        factors["resting_hr"] = float(recent_hr) if not pd.isna(recent_hr) else 0

    if "sleep_secs" in df.columns and not df["sleep_secs"].isna().all():
        avg_sleep = df["sleep_secs"].dropna().tail(7).mean()
        sleep_hours = avg_sleep / 3600 if not pd.isna(avg_sleep) else 7
        factors["sleep_hours"] = float(sleep_hours)
        if sleep_hours < 6:
            score -= 10
        elif sleep_hours < 7:
            score -= 5
        elif sleep_hours > 9:
            score -= 3

    score = max(0, min(100, score))
    return {"score": score, "factors": factors}


def detect_overtraining_risk(activities: list[dict], wellness: list[dict]) -> dict:
    risk = "low"
    indicators = []

    if len(activities) > 0:
        df_act = pd.DataFrame(activities)
        if "icu_tsb" in df_act.columns:
            last_tsb = df_act["icu_tsb"].dropna().tail(1)
            if not last_tsb.empty and last_tsb.values[0] < -30:
                risk = "high"
                indicators.append(f"TSB muito baixo: {last_tsb.values[0]:.1f}")
            elif not last_tsb.empty and last_tsb.values[0] < -15:
                risk = "medium"
                indicators.append(f"TSB baixo: {last_tsb.values[0]:.1f}")

    if len(wellness) > 0:
        df_well = pd.DataFrame(wellness)
        if "resting_hr" in df_well.columns:
            hr_values = df_well["resting_hr"].dropna().tail(7)
            if len(hr_values) >= 3 and hr_values.is_monotonic_increasing:
                risk = "medium"
                indicators.append("FC de repouso em tendência de alta")

    return {
        "risk": risk,
        "indicators": indicators if indicators else ["Nenhum sinal de risco detectado"],
    }


def calculate_hr_zone_distribution(activities: list[dict]) -> dict:
    df = pd.DataFrame(activities)
    if df.empty:
        return {"zones": {}}

    zones = {}
    for col in df.columns:
        if "hr_zone" in col.lower() or "icu_hr_zone" in col.lower():
            zone_name = col.replace("icu_hr_zone_", "Zona ").replace("_", " ")
            zones[zone_name] = float(df[col].sum())

    return {"zones": zones}
