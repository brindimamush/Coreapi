from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.merchant import Merchant

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