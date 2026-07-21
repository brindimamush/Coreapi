from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.repositories.subscription_plan_repo import SubscriptionPlanRepository
from app.schemas.subscription_plan import SubscriptionPlanResponse

router = APIRouter()

@router.get("", response_model=List[SubscriptionPlanResponse], status_code=200)
async def list_active_subscription_plans(db: AsyncSession = Depends(get_db)):
    """Public / Merchant endpoint returning only ACTIVE subscription plans."""
    repo = SubscriptionPlanRepository(db)
    plans = await repo.get_active_plans()
    return plans