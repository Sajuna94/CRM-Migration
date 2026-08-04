import enum
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from schema.base import Base

class EducationStatus(enum.Enum):
    unknown = "unknown"
    completed = "completed"
    studying = "studying"
    withdrawn = "withdrawn"

class EducationLevel(enum.Enum):
    secondary = "secondary"
    associate = "associate"
    bachelor = "bachelor"
    master = "master"
    doctorate = "doctorate"
    other = "other"


class TalentEducation(Base):
    __tablename__ = "talent_education"

    id = Column(Integer, primary_key=True)
    talent_id = Column(ForeignKey("talent.id"), nullable=False)

    school = Column(String, nullable=False)
    degree = Column(ENUM(EducationLevel, name="education_level", create_type=False))
    major = Column(String)

    status = Column(ENUM(EducationStatus, name="education_status", create_type=False), default="unknown")

    start_year = Column(SmallInteger)
    start_month = Column(SmallInteger)
    end_year = Column(SmallInteger)
    end_month = Column(SmallInteger)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
