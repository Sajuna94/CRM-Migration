from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from schema.base import Base

class TalentNote(Base):
    __tablename__ = "talent_note"

    id = Column(Integer, primary_key=True)
    talent_id = Column(ForeignKey("talent.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
