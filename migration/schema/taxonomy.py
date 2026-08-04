from sqlalchemy import Column, SmallInteger, String, DateTime, ForeignKey, Boolean
from schema.base import Base


class IndustryNode(Base):
    __tablename__ = "industry_node"

    id = Column(SmallInteger, primary_key=True)

    parent_id = Column(SmallInteger, ForeignKey("industry_node.id"))

    name = Column(String)

    is_active = Column(Boolean, default=True)

    sort_order = Column(SmallInteger, default=0)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class FunctionNode(Base):
    __tablename__ = "function_node"

    id = Column(SmallInteger, primary_key=True)

    parent_id = Column(SmallInteger, ForeignKey("function_node.id"))

    name = Column(String)

    is_active = Column(Boolean, default=True)

    sort_order = Column(SmallInteger, default=0)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)