from sqlalchemy import Column, Integer, String, DateTime, Enum, func
import enum

from schema.base import Base


class UserRole(enum.Enum):
    consultant = "consultant"
    manager = "manager"
    admin = "admin"

class UserStatus(enum.Enum):
    active = "active"
    invited = "invited"
    suspended = "suspended"

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    status = Column(Enum(UserStatus, name="user_status"), nullable=False, server_default="active")

    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
