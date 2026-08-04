import enum
from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.dialects.postgresql import ENUM, CITEXT
from sqlalchemy.sql import func
from schema.base import Base


# ==========================
# ENUM 定義
# ==========================

class CompanyRawStatus(enum.Enum):
    pending = "pending"    # 等待季度整理
    resolved = "resolved"  # 已找到 company，建立 alias 關聯
    ignored = "ignored"    # 保留原始紀錄，但不參與 search engine

# ==========================
# TABLE 定義
# ==========================

class CompanyRaw(Base):
    __tablename__ = "company_raw"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    status = Column(ENUM(CompanyRawStatus, name="company_raw_status"), nullable=False, server_default="pending")
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    law_name = Column(CITEXT, nullable=False)
    location = Column(Text, nullable=False)   # TODO: 目前純文字
    tax_id = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CompanyAlias(Base):
    __tablename__ = "company_alias"

    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    name = Column(CITEXT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("company_id", "name", name="company_alias_pk"),
    )
