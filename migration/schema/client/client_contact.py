from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from schema.base import Base

class ClientContact(Base):
    __tablename__ = "client_contact"

    id = Column(Integer, primary_key=True, autoincrement=True)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    talent_id = Column(UUID(as_uuid=True), ForeignKey("talent.id"), nullable=False)

    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("client_id", "talent_id", name="client_contact_unique"),
    )
