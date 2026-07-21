import uuid
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
import enum

class MerchantStatus(str, enum.Enum):
    REGISTERING = "REGISTERING"   # used during conversation? we'll keep it simple
    REGISTERED = "REGISTERED"

class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    telebirr_name: Mapped[str] = mapped_column(String(255), nullable=False)
    telebirr_phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    status: Mapped[MerchantStatus] = mapped_column(
        SAEnum(MerchantStatus, name="merchant_status"),
        default=MerchantStatus.REGISTERED,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )