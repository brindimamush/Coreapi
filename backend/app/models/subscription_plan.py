import uuid
import enum
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import String, Text, Numeric, Integer, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class PlanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="ETB", nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Limits (NULL represents Unlimited)
    max_api_keys: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_services: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_monthly_invoices: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[PlanStatus] = mapped_column(
        SAEnum(PlanStatus, name="plan_status"),
        default=PlanStatus.DRAFT,
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )