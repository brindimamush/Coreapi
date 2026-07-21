from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models here to ensure they are registered
# from app.models.merchant import Merchant       # noqa: E402, F401
# from app.models.audit_log import AuditLog      # noqa: E402, F401