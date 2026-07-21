import re
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator, EmailStr

class MerchantRegistrationRequest(BaseModel):
    telegram_id: int
    telegram_username: str | None = None
    telegram_first_name: str
    telegram_last_name: str | None = None
    business_name: str
    business_email: EmailStr
    phone_number: str
    telebirr_name: str
    telebirr_phone: str

    @field_validator("business_name")
    @classmethod
    def validate_business_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2 or len(v) > 100:
            raise ValueError("Business name must be between 2 and 100 characters")
        return v

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        # strip all non-digit characters except leading +
        v = re.sub(r"[^\d+]", "", v)
        # convert international to local
        if v.startswith("+251"):
            v = "0" + v[4:]
        elif v.startswith("251"):
            v = "0" + v[3:]
        if not re.match(r"^09\d{8}$", v):
            raise ValueError("Invalid Ethiopian phone number. Must be like 0911223344")
        return v

    @field_validator("telebirr_phone")
    @classmethod
    def validate_telebirr_phone(cls, v: str) -> str:
        v = re.sub(r"[^\d+]", "", v)
        if v.startswith("+251"):
            v = "0" + v[4:]
        elif v.startswith("251"):
            v = "0" + v[3:]
        if not re.match(r"^09\d{8}$", v):
            raise ValueError("Invalid Telebirr number. Must be like 0911223344")
        return v

class MerchantResponse(BaseModel):
    id: UUID
    telegram_id: int
    business_name: str
    business_email: str
    phone_number: str
    telebirr_name: str
    telebirr_phone: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True