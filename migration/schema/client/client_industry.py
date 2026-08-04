from sqlalchemy import Column, Integer, ForeignKey
from schema.base import Base

class ClientIndustry(Base):
    __tablename__ = "client_industry"

    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), primary_key=True)
    industry_id = Column(Integer, ForeignKey("industry_node.id"), primary_key=True)
