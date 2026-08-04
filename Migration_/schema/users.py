from enum import Enum
from datetime import datetime
from core.column import Column
from core.table import Table

class UserRole(str, Enum):
    consultant = "consultant"
    manager = "manager"
    admin = "admin"

class UserStatus(str, Enum):
    active = "active"
    invited = "invited"
    suspended = "suspended"

class User(Table):
    def __init__(self):
        super().__init__("user", {
            "id": Column("integer", pk=True, auto_increment=True),
            "name": Column("text", not_null=True, unique=True, check=lambda v: len(v) <= 50),
            "email": Column("citext", not_null=True, unique=True, check=lambda v: "@" in v),
            "role": Column("user_role", not_null=True),   # 對應 Enum
            "status": Column("user_status", not_null=True, default=UserStatus.active),
            "create_at": Column("timestamptz", not_null=True, default=datetime.now)
        })
