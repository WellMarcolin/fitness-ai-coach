import httpx
from datetime import date
from typing import Optional

from app.config import settings

BASE_URL = "https://intervals.icu/api/v1"


class IntervalsClient:
    def __init__(self):
        self.athlete_id = settings.intervals_athlete_id
        self.client = httpx.AsyncClient(
            base_url=BASE_URL,
            auth=("API_KEY", settings.intervals_api_key),
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

    async def close(self):
        await self.client.aclose()

    # === Athlete ===
    async def get_athlete(self) -> dict:
        r = await self.client.get(f"/athlete/{self.athlete_id}")
        r.raise_for_status()
        return r.json()

    # === Activities ===
    async def get_activities(
        self,
        oldest: date,
        newest: date,
        fields: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict]:
        params = {
            "oldest": oldest.isoformat(),
            "newest": newest.isoformat(),
            "limit": limit,
        }
        if fields:
            params["fields"] = fields
        r = await self.client.get(
            f"/athlete/{self.athlete_id}/activities",
            params=params,
        )
        r.raise_for_status()
        return r.json()

    async def get_activity(self, activity_id: str) -> dict:
        r = await self.client.get(f"/activity/{activity_id}")
        r.raise_for_status()
        return r.json()

    async def get_activity_streams(self, activity_id: str) -> dict:
        r = await self.client.get(f"/activity/{activity_id}/streams.csv")
        r.raise_for_status()
        return r.text

    # === Events (Calendar) ===
    async def get_events(
        self,
        oldest: date,
        newest: date,
        category: Optional[str] = None,
    ) -> list[dict]:
        params = {"oldest": oldest.isoformat(), "newest": newest.isoformat()}
        if category:
            params["category"] = category
        r = await self.client.get(
            f"/athlete/{self.athlete_id}/events",
            params=params,
        )
        r.raise_for_status()
        return r.json()

    async def create_event(self, event_data: dict) -> dict:
        r = await self.client.post(
            f"/athlete/{self.athlete_id}/events",
            json=event_data,
        )
        r.raise_for_status()
        return r.json()

    async def update_event(self, event_id: str, event_data: dict) -> dict:
        r = await self.client.put(
            f"/athlete/{self.athlete_id}/events/{event_id}",
            json=event_data,
        )
        r.raise_for_status()
        return r.json()

    async def delete_event(self, event_id: str):
        r = await self.client.delete(
            f"/athlete/{self.athlete_id}/events/{event_id}",
        )
        r.raise_for_status()

    async def bulk_create_events(self, events: list[dict]) -> dict:
        r = await self.client.post(
            f"/athlete/{self.athlete_id}/events/bulk",
            json=events,
        )
        r.raise_for_status()
        return r.json()

    # === Wellness ===
    async def get_wellness(self, oldest: date, newest: date) -> list[dict]:
        params = {"oldest": oldest.isoformat(), "newest": newest.isoformat()}
        r = await self.client.get(
            f"/athlete/{self.athlete_id}/wellness",
            params=params,
        )
        r.raise_for_status()
        return r.json()

    async def update_wellness(self, record_date: str, data: dict) -> dict:
        r = await self.client.put(
            f"/athlete/{self.athlete_id}/wellness/{record_date}",
            json=data,
        )
        r.raise_for_status()
        return r.json()

    # === Workouts ===
    async def get_workouts(self) -> list[dict]:
        r = await self.client.get(f"/athlete/{self.athlete_id}/workouts")
        r.raise_for_status()
        return r.json()

    # === Sport Settings ===
    async def get_sport_settings(self) -> dict:
        r = await self.client.get(f"/athlete/{self.athlete_id}/sport-settings")
        r.raise_for_status()
        return r.json()

    async def update_sport_settings(self, sport: str, data: dict) -> dict:
        r = await self.client.put(
            f"/athlete/{self.athlete_id}/sport-settings/{sport}",
            json=data,
        )
        r.raise_for_status()
        return r.json()


