from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.redis import get_redis
import redis.asyncio as redis

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@router.get("/health/database")
async def database_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"database": "connected"}
    except Exception as e:
        return {"database": "unavailable", "error": str(e)}

@router.get("/health/redis")
async def redis_health(client: redis.Redis = Depends(get_redis)):
    try:
        await client.ping()
        return {"redis": "connected"}
    except Exception as e:
        return {"redis": "unavailable", "error": str(e)}