import enum
from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from schema.base import Base

# ==========================
# ENUM 定義 (保留在同檔案)
# ==========================
class ClientStatus(enum.Enum):
    lead = "lead"        # 加入觀察名單
    ongoing = "ongoing"  # 開發中
    open = "open"        # 已簽約

# ==========================
# TABLE 定義
# ==========================
class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # owner
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sales_owner_id = Column(Integer, ForeignKey("users.id"))

    # company
    company_id = Column(Integer, ForeignKey("company.id"))
    company_raw_id = Column(Integer, ForeignKey("company_raw.id"))

    # status
    status = Column(ENUM(ClientStatus, name="client_status"), nullable=False, server_default="lead")

    note = Column(Text)

    # audit
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "NOT (company_id IS NOT NULL AND company_raw_id IS NOT NULL)",
            name="client_company_reference_check"
        ),
    )
