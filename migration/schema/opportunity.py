import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.dialects.postgresql import ENUM
from schema.base import Base

class OpportunityStatus(enum.Enum):
    ongoing = "ongoing"
    failed = "failed"
    placed = "placed"
    pending = "pending"

class Opportunity(Base):
    __tablename__ = "opportunity"

    id = Column(Integer, primary_key=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    client_contact_id = Column(Integer, ForeignKey("client_contact.id"), nullable=False)

    title = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    headcount = Column(Integer, nullable=False)

    status = Column(ENUM(OpportunityStatus, name="opportunity_status", create_type=False), nullable=False, default="ongoing")
    is_priority = Column(Boolean, nullable=False, default=False)

    opened_at = Column(DateTime, nullable=False)
    note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class OpportunityIndustry(Base):
    __tablename__ = "opportunity_industry"

    opportunity_id = Column(Integer, ForeignKey("opportunity.id", ondelete="CASCADE"), primary_key=True)
    industry_id = Column(Integer, ForeignKey("industry_node.id"), primary_key=True)

class OpportunityFunction(Base):
    __tablename__ = "opportunity_function"

    opportunity_id = Column(Integer, ForeignKey("opportunity.id", ondelete="CASCADE"), primary_key=True)
    function_id = Column(Integer, ForeignKey("function_node.id"), primary_key=True)
