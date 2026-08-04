import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


from core.context import Context
from core.context import Context
import csv


ctx = Context()

table = ctx.table("users")

with open(
    "mappings/users.csv",
    encoding="utf-8-sig"
) as f:

    for row in csv.DictReader(f):
        table.insert({
            "id": int(row["id"]),
            "name": row["name"]
        })


table.export_csv(
    "output/users.csv"
)