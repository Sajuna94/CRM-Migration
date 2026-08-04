from sqlalchemy import Column, Integer, Text, DateTime, Enum, ForeignKey, func
import enum
from schema.base import Base


class NoteTargetType(enum.Enum):
    talent = "talent"
    client = "client"
    opportunity = "opportunity"

class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_type = Column(Enum(NoteTargetType, name="note_target_type", create_type=False), nullable=False)
    target_id = Column(Text, nullable=False)

    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
