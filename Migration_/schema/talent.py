from core.table import Table
from core.column import Column
from enum import Enum
from datetime import datetime

class TalentStatus(str, Enum):
    unknown = "unknown"
    hired = "hired"
    open = "open"
    archived = "archived"
    active = "active"

class ExpectedSalaryStatus(str, Enum):
    negotiable = "negotiable"
    company_policy = "company_policy"

class CandidateSex(str, Enum):
    male = "male"
    female = "female"

class TalentSourceType(str, Enum):
    import_ = "import"
    platform = "platform"
    other = "other"


class Talent(Table):
    def __init__(self):
        super().__init__("talent", {
            "id": Column("uuid", pk=True, default="gen_random_uuid()"),
            "created_by_id": Column("integer", not_null=True),
            "source_id": Column("integer", not_null=True),
            "name_english": Column("text"),
            "name_chinese": Column("text"),
            "email": Column("citext", unique=True),
            "phone_country_code": Column("varchar(3)"),
            "phone_number": Column("varchar(14)"),
            "phone_extension": Column("varchar(10)"),
            "cv_url": Column("text"),
            "linked_urls": Column("text"),
            "ps_url": Column("text"),
            "company_id": Column("integer"),
            "company_raw_id": Column("integer"),
            "current_title": Column("text"),
            "current_salary": Column("integer"),
            "status": Column("talent_status"),
            "expected_salary": Column("integer"),
            "expected_salary_status": Column("expected_salary_status"),
            "sex": Column("candidate_sex"),
            "birth_year": Column("smallint"),
            "birth_month": Column("smallint"),
            "birth_day": Column("smallint"),
            "highest_education": Column("education_level"),
            "highest_school": Column("text"),
            "highest_major": Column("text"),
            "created_at": Column("timestamptz", default=datetime.now),
            "updated_at": Column("timestamptz", default=datetime.now)
        })

    def insert(self, **kwargs):
        # 檢查至少要有名字
        if not kwargs.get("name_english") and not kwargs.get("name_chinese"):
            raise ValueError("Talent must have at least one name (English or Chinese).")

        # 檢查至少要有聯絡方式
        if not kwargs.get("phone_number") and not kwargs.get("email") and not kwargs.get("cv_url"):
            raise ValueError("Talent must have at least one contact method (phone, email, or CV).")

        # 只禁止同時有值，允許同時為 None
        if kwargs.get("company_id") is not None and kwargs.get("company_raw_id") is not None:
            raise ValueError("Talent cannot reference both company_id and company_raw_id.")

        # 檢查生日 month/day 必須同時存在或同時為空
        if (kwargs.get("birth_month") is None) != (kwargs.get("birth_day") is None):
            raise ValueError("Talent birth_month and birth_day must both be null or both provided.")

        # Enum 檢查
        if kwargs.get("status") and kwargs["status"] not in TalentStatus._value2member_map_:
            raise ValueError(f"Invalid TalentStatus: {kwargs['status']}")
        if kwargs.get("expected_salary_status") and kwargs["expected_salary_status"] not in ExpectedSalaryStatus._value2member_map_:
            raise ValueError(f"Invalid ExpectedSalaryStatus: {kwargs['expected_salary_status']}")
        if kwargs.get("sex") and kwargs["sex"] not in CandidateSex._value2member_map_:
            raise ValueError(f"Invalid CandidateSex: {kwargs['sex']}")

        return super().insert(**kwargs)

talent = Talent()
