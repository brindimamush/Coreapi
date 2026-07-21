from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.merchant import Merchant
from datetime import datetime, timedelta, timezone

class MerchantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[Merchant]:
        result = await self.session.execute(
            select(Merchant).where(Merchant.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Merchant]:
        result = await self.session.execute(
            select(Merchant).where(Merchant.business_email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[Merchant]:
        result = await self.session.execute(
            select(Merchant).where(Merchant.phone_number == phone)
        )
        return result.scalar_one_or_none()

    async def get_by_telebirr_phone(self, telebirr_phone: str) -> Optional[Merchant]:
        result = await self.session.execute(
            select(Merchant).where(Merchant.telebirr_phone == telebirr_phone)
        )
        return result.scalar_one_or_none()

    async def create(self, merchant: Merchant) -> Merchant:
        self.session.add(merchant)
        await self.session.flush()
        return merchant
    
    async def get_all_paginated(self, skip: int = 0, limit: int = 10, search: str = "") -> tuple[list[Merchant], int]:
        query = select(Merchant)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (Merchant.business_name.ilike(search_term)) |
                (Merchant.business_email.ilike(search_term)) |
                (Merchant.phone_number.ilike(search_term))
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)
        
        # Get paginated data
        query = query.order_by(Merchant.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total or 0

    async def get_by_id(self, merchant_id: str) -> Optional[Merchant]:
        result = await self.session.execute(
            select(Merchant).where(Merchant.id == merchant_id)
        )
        return result.scalar_one_or_none()

    async def get_stats(self) -> dict:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Total merchants
        total = await self.session.scalar(select(func.count()).select_from(Merchant))
        
        # Registered today
        today_count = await self.session.scalar(
            select(func.count()).select_from(Merchant).where(Merchant.created_at >= today_start)
        )
        
        return {
            "totalMerchants": total or 0,
            "registeredToday": today_count or 0,
            "activeRate": 100, # Placeholder until status logic is expanded
            "registrationTrend": [] # Implement time-series aggregation here as needed
        }