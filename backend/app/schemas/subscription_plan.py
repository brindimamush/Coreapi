import re
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.subscription_plan import PlanStatus

class SubscriptionPlanCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    currency: str = Field(default="ETB", min_length=2, max_length=10)
    duration_days: int = Field(..., ge=1)
    max_api_keys: Optional[int] = Field(default=None, ge=1)
    max_services: Optional[int] = Field(default=None, ge=1)
    max_monthly_invoices: Optional[int] = Field(default=None, ge=1)
    display_order: int = Field(default=1, ge=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Plan name cannot be empty")
        return v

class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field(None, min_length=2, max_length=10)
    duration_days: Optional[int] = Field(None, ge=1)
    max_api_keys: Optional[int] = Field(None, ge=1)
    max_services: Optional[int] = Field(None, ge=1)
    max_monthly_invoices: Optional[int] = Field(None, ge=1)
    display_order: Optional[int] = Field(None, ge=1)

class StatusTransitionRequest(BaseModel):
    status: PlanStatus

class SubscriptionPlanResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    price: Decimal
    currency: str
    duration_days: int
    max_api_keys: Optional[int]
    max_services: Optional[int]
    max_monthly_invoices: Optional[int]
    status: PlanStatus
    display_order: int
    created_by: Optional[str]
    updated_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True