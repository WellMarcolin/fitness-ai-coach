from fastapi import APIRouter, HTTPException, Query
from datetime import date, timedelta

from app.core.intervals_client import IntervalsClient
from app.models.schemas import ActivitySummary, WellnessRecord

router = APIRouter()


async def get_client() -> IntervalsClient:
    client = IntervalsClient()
    return client


@router.get("/athlete")
async def get_athlete():
    client = await get_client()
    try:
        data = await client.get_athlete()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/activities")
async def get_activities(
    days: int = Query(30, ge=1, le=365),
    fields: str = Query(
        "id,name,start_date_local,type,distance,moving_time,average_heartrate,max_heartrate,icu_training_load,icu_atl,icu_ctl,icu_tsb,weighted_average_watts,calories"
    ),
):
    client = await get_client()
    try:
        newest = date.today()
        oldest = newest - timedelta(days=days)
        data = await client.get_activities(oldest=oldest, newest=newest, fields=fields)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/activities/{activity_id}")
async def get_activity(activity_id: str):
    client = await get_client()
    try:
        data = await client.get_activity(activity_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/activities/{activity_id}/streams")
async def get_activity_streams(activity_id: str):
    client = await get_client()
    try:
        data = await client.get_activity_streams(activity_id)
        return {"csv": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/events")
async def get_events(
    days: int = Query(14, ge=1, le=365),
    category: str = Query(None),
):
    client = await get_client()
    try:
        newest = date.today() + timedelta(days=30)
        oldest = date.today() - timedelta(days=days)
        data = await client.get_events(oldest=oldest, newest=newest, category=category)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/events")
async def create_event(event_data: dict):
    client = await get_client()
    try:
        data = await client.create_event(event_data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.put("/events/{event_id}")
async def update_event(event_id: str, event_data: dict):
    client = await get_client()
    try:
        data = await client.update_event(event_id, event_data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.delete("/events/{event_id}")
async def delete_event(event_id: str):
    client = await get_client()
    try:
        await client.delete_event(event_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/wellness")
async def get_wellness(days: int = Query(30, ge=1, le=365)):
    client = await get_client()
    try:
        newest = date.today()
        oldest = newest - timedelta(days=days)
        data = await client.get_wellness(oldest=oldest, newest=newest)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.put("/wellness/{record_date}")
async def update_wellness(record_date: str, data: dict):
    client = await get_client()
    try:
        result = await client.update_wellness(record_date, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/workouts")
async def get_workouts():
    client = await get_client()
    try:
        data = await client.get_workouts()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/sport-settings")
async def get_sport_settings():
    client = await get_client()
    try:
        data = await client.get_sport_settings()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()
