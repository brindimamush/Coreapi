from fastapi import APIRouter, Depends, Request, HTTPException, Security, status, BackgroundTasks
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.merchant import MerchantRegistrationRequest, MerchantResponse
from app.services.merchant_service import MerchantService
from app.core.config import settings
from typing import Optional

router = APIRouter()
api_key_header = APIKeyHeader(name="X-Internal-API-Key", auto_error=True)

async def verify_internal_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return api_key

@router.get("/check/{telegram_id}", status_code=200)
async def check_merchant_registration(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(verify_internal_api_key)
):
    service = MerchantService(db)
    merchant = await service.repo.get_by_telegram_id(telegram_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return {"status": merchant.status, "merchant_id": str(merchant.id)}

@router.post("/register", response_model=MerchantResponse, status_code=201)
async def register_merchant(
    payload: MerchantRegistrationRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(verify_internal_api_key),
):
    service = MerchantService(db)
    ip = request.client.host if request.client else None
    
    # We pass background_tasks to the service to handle audit logs asynchronously
    merchant = await service.register(payload, background_tasks=background_tasks, ip_address=ip)
    return merchant

@router.get("", status_code=200)
async def list_merchants(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(verify_internal_api_key)
):
    service = MerchantService(db)
    skip = (page - 1) * limit
    merchants, total = await service.repo.get_all_paginated(skip=skip, limit=limit, search=search)
    
    return {
        "data": merchants,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/stats", status_code=200)
async def get_merchant_stats(
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(verify_internal_api_key)
):
    service = MerchantService(db)
    stats = await service.repo.get_stats()
    return stats

@router.get("/{merchant_id}", status_code=200)
async def get_merchant(
    merchant_id: str,
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(verify_internal_api_key)
):
    service = MerchantService(db)
    merchant = await service.repo.get_by_id(merchant_id)
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return merchant