from sqlalchemy import Column, SmallInteger, ForeignKey
from schema.base import Base

class TalentFunction(Base):
    __tablename__ = "talent_function"

    talent_id = Column(ForeignKey("talent.id"), primary_key=True)
    function_id = Column(SmallInteger, ForeignKey("function_node.id"), primary_key=True)
