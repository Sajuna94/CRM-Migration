from core.table import Table
from core.column import Column
from enum import Enum
from datetime import datetime

class ClientStatus(str, Enum):
    lead = "lead"        # 加入觀察名單
    ongoing = "ongoing"  # 開發中
    open = "open"        # 已簽約

class Client(Table):
    def __init__(self):
        super().__init__("client", {
            "id": Column("integer", pk=True, auto_increment=True),
            "created_by_id": Column("integer", not_null=True),
            "sales_owner_id": Column("integer"),
            "company_id": Column("integer"),
            "company_raw_id": Column("integer"),
            "status": Column("client_status", default="'lead'"),
            "note": Column("text"),
            "created_at": Column("timestamptz", default=datetime.now),
            "updated_at": Column("timestamptz", default=datetime.now)
        })

    def insert(self, **kwargs):
        # 檢查 company_id 和 company_raw_id 不可同時存在
        if kwargs.get("company_id") is not None and kwargs.get("company_raw_id") is not None:
            raise ValueError("Client cannot reference both company_id and company_raw_id.")
    
        if kwargs.get("status") and kwargs["status"] not in ClientStatus._value2member_map_:
            raise ValueError(f"Invalid ClientStatus: {kwargs['status']}")
        
        return super().insert(**kwargs)


client = Client()
