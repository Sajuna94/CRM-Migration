from core.table import Table


class Context:

    def __init__(self):

        users = Table(
            name="users",
            columns=[
                "id",
                "name"
            ],
            primary_key="id"
        )

        company_raw = Table(
            name="company_raw",
            columns=[
                "id",
                "name",
                "status",
                "created_by_id",
                "created_at",
                "updated_at"
            ],
            primary_key="id",
            unique=[
                ("name",)
            ],
            foreign_keys={
                "created_by_id": users
            }
        )

        talent = Table(
            name="talent",
            columns=[
                "id",
                "created_by_id",
                "source_id",
                "name_english",
                "name_chinese",
                "email",
                "phone_country_code",
                "phone_number",
                "phone_extension",
                "cv_url",
                "linked_urls",
                "ps_url",
                "company_id",
                "company_raw_id",
                "current_title",
                "current_salary",
                "status",
                "expected_salary",
                "expected_salary_status",
                "sex",
                "birth_year",
                "birth_month",
                "birth_day",
                "highest_education",
                "highest_school",
                "highest_major",
                "created_at",
                "updated_at"
            ],
            primary_key="id",
            foreign_keys={
                "created_by_id": users,
                "company_raw_id": company_raw
            }
        )

        client = Table(
            name="client",
            columns=[
                "id",
                "created_by_id",
                "sales_owner_id",
                "company_id",
                "company_raw_id",
                "status",
                "note",
                "created_at",
                "updated_at"
            ],
            primary_key="id",
            foreign_keys={
                "created_by_id": users,
                "sales_owner_id": users,
                "company_raw_id": company_raw
            }
        )

        self.tables = {
            "users": users,
            "company_raw": company_raw,
            "talent": talent,
            "client": client
        }


    def table(self, name):
        return self.tables[name]