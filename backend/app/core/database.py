from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# === Cache Models ===
class CachedActivity(Base):
    __tablename__ = "cached_activities"

    id = Column(String, primary_key=True)
    athlete_id = Column(String, index=True)
    data = Column(JSON)
    synced_at = Column(DateTime)


class CachedWellness(Base):
    __tablename__ = "cached_wellness"

    id = Column(String, primary_key=True)  # YYYY-MM-DD
    athlete_id = Column(String, index=True)
    data = Column(JSON)
    synced_at = Column(DateTime)


class CachedEvent(Base):
    __tablename__ = "cached_events"

    id = Column(String, primary_key=True)
    athlete_id = Column(String, index=True)
    data = Column(JSON)
    synced_at = Column(DateTime)


class AgentPrompt(Base):
    __tablename__ = "agent_prompts"

    agent_type = Column(String, primary_key=True)
    system_prompt = Column(Text)
    updated_at = Column(DateTime)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
