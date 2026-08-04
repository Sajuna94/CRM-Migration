from core.context import Context
from core.resolver import Resolver

from importers.users import import_users
from importers.company_raw import import_company_raw


ctx = Context()


import_users(
    ctx.table("users"),
    "mappings/users.csv"
)


resolver = Resolver(
    ctx.table("users")
)


import_company_raw(
    ctx.table("company_raw"),
    resolver,
    "sample/candidate.csv",
    company_field="公司",
    owner_field="擁有者",
    created_at_field="添加日期"
)


ctx.table("users").export_csv(
    "output/users.csv"
)

ctx.table("company_raw").export_csv(
    "output/company_raw.csv"
)