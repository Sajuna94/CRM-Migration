from core.table import Table
from core.column import Column
from datetime import datetime
from enum import Enum

class CompanyRawStatus(str, Enum):
    pending = "pending"   # 等待季度整理
    resolved = "resolved" # 已找到 company，建立 alias 關聯
    ignored = "ignored"   # 保留原始紀錄，但不參與 search engine

class CompanyRaw(Table):
    def __init__(self):
        super().__init__("company_raw", {
            "id": Column("integer", pk=True, auto_increment=True),
            "name": Column("text", not_null=True, unique=True),
            "status": Column("company_raw_status", default="'pending'"),
            "created_by_id": Column("integer", not_null=True),
            "created_at": Column("timestamptz", default=datetime.now),
            "updated_at": Column("timestamptz", default=datetime.now)
        })
        
    def insert(self, **kwargs):
        if kwargs.get("status") and kwargs["status"] not in CompanyRawStatus._value2member_map_:
            raise ValueError(f"Invalid CompanyRawStatus: {kwargs['status']}")
        return super().insert(**kwargs)


company_raw = CompanyRaw()
