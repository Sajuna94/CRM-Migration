from sqlalchemy import Column, SmallInteger, ForeignKey
from schema.base import Base

class TalentIndustry(Base):
    __tablename__ = "talent_industry"

    talent_id = Column(ForeignKey("talent.id"), primary_key=True)
    industry_id = Column(SmallInteger, ForeignKey("industry_node.id"), primary_key=True)
