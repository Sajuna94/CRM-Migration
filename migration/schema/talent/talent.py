import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, ENUM, CITEXT
from schema.base import Base

class TalentStatus(enum.Enum):
    unknown = "unknown"
    hired = "hired"
    open = "open"
    archived = "archived"
    active = "active"

class ExpectedSalaryStatus(enum.Enum):
    negotiable = "negotiable"
    company_policy = "company_policy"

class CandidateSex(enum.Enum):
    male = "male"
    female = "female"

class EducationLevel(enum.Enum):
    secondary = "secondary"
    associate = "associate"
    bachelor = "bachelor"
    master = "master"
    doctorate = "doctorate"
    other = "other"


class Talent(Base):
    __tablename__ = "talent"

    id = Column(UUID(as_uuid=True), primary_key=True)

    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("talent_source.id"), nullable=False)

    name_english = Column(String)
    name_chinese = Column(String)

    email = Column(CITEXT, unique=True)
    phone_country_code = Column(String(3))
    phone_number = Column(String(14))
    phone_extension = Column(String(10))

    cv_url = Column(String)
    linked_urls = Column(String)
    ps_url = Column(String)

    company_id = Column(Integer, ForeignKey("company.id"))
    company_raw_id = Column(Integer, ForeignKey("company_raw.id"))
    company_confidential = Column(Boolean, default=False)

    current_title = Column(String)
    current_salary = Column(Integer)

    status = Column(ENUM(TalentStatus, name="talent_status", create_type=False))
    expected_salary = Column(Integer)
    expected_salary_status = Column(ENUM(ExpectedSalaryStatus, name="expected_salary_status", create_type=False))

    sex = Column(ENUM(CandidateSex, name="candidate_sex", create_type=False))
    birth_year = Column(SmallInteger)
    birth_month = Column(SmallInteger)
    birth_day = Column(SmallInteger)

    highest_education = Column(ENUM(EducationLevel, name="education_level", create_type=False))
    highest_school = Column(String)
    highest_major = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
