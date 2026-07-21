from typing import Optional
from fastapi import APIRouter, Depends, Request, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.subscription_plan import (
    SubscriptionPlanCreate,
    SubscriptionPlanUpdate,
    SubscriptionPlanResponse,
    StatusTransitionRequest,
)
from app.services.subscription_plan_service import SubscriptionPlanService
from app.models.subscription_plan import PlanStatus
from app.core.config import settings

router = APIRouter()
api_key_header = APIKeyHeader(name="X-Internal-API-Key", auto_error=True)

async def verify_admin_key(api_key: str = Security(api_key_header)):
    if api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return api_key

@router.post("", response_model=SubscriptionPlanResponse, status_code=201)
async def create_plan(
    payload: SubscriptionPlanCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _key: str = Depends(verify_admin_key),
):
    service = SubscriptionPlanService(db)
    ip = request.client.host if request.client else None
    return await service.create_plan(payload, admin_id="platform_admin", ip_address=ip)

@router.get("", status_code=200)
async def list_admin_plans(
    page: int = 1,
    limit: int = 20,
    search: str = "",
    status_filter: Optional[PlanStatus] = None,
    db: AsyncSession = Depends(get_db),
    _key: str = Depends(verify_admin_key),
):
    service = SubscriptionPlanService(db)
    skip = (page - 1) * limit
    plans, total = await service.repo.get_all_paginated(
        skip=skip, limit=limit, search=search, status=status_filter
    )
    return {"data": plans, "total": total, "page": page, "limit": limit}

@router.get("/stats", status_code=200)
async def get_plan_stats(
    db: AsyncSession = Depends(get_db),
    _key: str = Depends(verify_admin_key)
):
    service = SubscriptionPlanService(db)
    return await service.repo.get_stats()

@router.put("/{plan_id}", response_model=SubscriptionPlanResponse, status_code=200)
async def update_plan(
    plan_id: str,
    payload: SubscriptionPlanUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _key: str = Depends(verify_admin_key),
):
    service = SubscriptionPlanService(db)
    ip = request.client.host if request.client else None
    return await service.update_plan(plan_id, payload, admin_id="platform_admin", ip_address=ip)

@router.patch("/{plan_id}/status", response_model=SubscriptionPlanResponse, status_code=200)
async def transition_plan_status(
    plan_id: str,
    payload: StatusTransitionRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _key: str = Depends(verify_admin_key),
):
    service = SubscriptionPlanService(db)
    ip = request.client.host if request.client else None
    return await service.transition_status(plan_id, payload.status, admin_id="platform_admin", ip_address=ip)