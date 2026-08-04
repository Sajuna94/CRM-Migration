import enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from schema.base import Base

class TalentSourceType(enum.Enum):
    import_ = "import"
    platform = "platform"
    other = "other"


class TalentSource(Base):
    __tablename__ = "talent_source"

    id = Column(Integer, primary_key=True)
    type = Column(ENUM(TalentSourceType, name="talent_source_type", create_type=False), nullable=False)
    name = Column(String, nullable=False)
