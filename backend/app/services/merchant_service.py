import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.merchant_repo import MerchantRepository
from app.models.merchant import Merchant, MerchantStatus
from app.models.audit_log import AuditLog
from app.schemas.merchant import MerchantRegistrationRequest
from fastapi import HTTPException, status
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

class MerchantService:
    def __init__(self, session: AsyncSession):
        self.repo = MerchantRepository(session)
        self.session = session

    async def create_audit_log_task(self, audit_log: AuditLog):
        self.session.add(audit_log)
        await self.session.commit()

    async def register(self, request: MerchantRegistrationRequest, background_tasks, ip_address: str | None = None) -> Merchant:
        # Normalize email
        email = request.business_email.lower()

        # Check for existing duplicates
        if await self.repo.get_by_telegram_id(request.telegram_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Telegram account is already registered.",
            )
        if await self.repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )
        if await self.repo.get_by_phone(request.phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number already exists.",
            )
        if await self.repo.get_by_telebirr_phone(request.telebirr_phone):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Telebirr number is already registered.",
            )
        
        # Create merchant entity
        merchant = Merchant(
            telegram_id=request.telegram_id,
            telegram_username=request.telegram_username,
            telegram_first_name=request.telegram_first_name,
            telegram_last_name=request.telegram_last_name,
            business_name=request.business_name.strip(),
            business_email=email,
            phone_number=request.phone_number,
            telebirr_name=request.telebirr_name.strip(),
            telebirr_phone=request.telebirr_phone,
            status=MerchantStatus.REGISTERED,
        )
        await self.repo.create(merchant)
        await self.session.commit()
        await self.session.refresh(merchant)
        # Create audit log entry
        audit = AuditLog(
            actor_type="merchant",
            actor_id=str(merchant.id),
            action="MERCHANT_REGISTERED",
            entity="merchant",
            entity_id=str(merchant.id),
            new_values=request.model_dump(),
            ip_address=ip_address,
        )

        background_tasks.add_task(self.create_audit_log_task, audit)

        logger.info("Merchant registered", extra={"merchant_id": str(merchant.id), "telegram_id": merchant.telegram_id})
        return merchant