import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import csv
from core.context import Context
from core.resolver import Resolver

ctx = Context()

users = ctx.table("users")

with open("output/users.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        users.insert({"id": int(row["id"]), "name": row["name"]})

resolver = Resolver(users)

company_raw = ctx.table("company_raw")
talent = ctx.table("talent")
client = ctx.table("client")

def get_company_raw_id(name, created_by_id, created_at):
    if not name:
        return None

    exists = company_raw.find_by_unique("name", name)

    if exists:
        return exists["id"]

    company_raw.insert({
        "name": name,
        "status": "pending",
        "created_by_id": created_by_id,
        "created_at": created_at,
        "updated_at": created_at
    })

    return company_raw.rows[-1]["id"]


with open("sample/candidate.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        company_raw_id = get_company_raw_id(
            row["公司"],
            resolver.user_id(row["擁有者"]),
            row["添加日期"]
        )

        talent.insert({
            "id": row["EID"],
            "company_raw_id": company_raw_id
        })


with open("sample/client.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        company_raw_id = get_company_raw_id(
            row["公司名稱"],
            resolver.user_id(row["添加人"]),
            row["添加日期"]
        )

        client.insert({
            "id": row["Client_id"],
            "company_raw_id": company_raw_id
        })


company_raw.export_csv("output/company_raw.csv")
talent.export_csv("output/talent.csv")
client.export_csv("output/client.csv")