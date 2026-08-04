import pandas as pd
from datetime import datetime
from schema.client import Client
from schema.users import Users
from schema.company import CompanyRaw
from pipeline.db import SessionLocal
import os

def run(client_path="input/client.csv"):
    session = SessionLocal()
    rejected_rows = []

    df = pd.read_csv(client_path)
    df = df.replace({pd.NA: None, float("nan"): None})

    for _, row in df.iterrows():
        # ==========================
        # reject validation
        # ==========================
        if not row.get("公司名稱"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_company_name"
            rejected_rows.append(rejected)
            continue

        # 找 BD (sales_owner)
        bd_name = str(row.get("BD") or "").strip()
        bd_user = session.query(Users).filter_by(name=bd_name).first() if bd_name else None

        # 找公司
        company_name = str(row.get("公司名稱") or "").strip()
        company_raw = session.query(CompanyRaw).filter_by(name=company_name).first()

        # 狀態 (Enum: lead / ongoing / open)
        # status = str(row.get("類型") or "lead").strip().lower()
        # if status not in ["lead", "ongoing", "open"]:
        #     status = "lead"

        # 匯入 client
        client = Client(
            created_by_id=1,  # 預設系統匯入者，可改成實際 user.id
            sales_owner_id=bd_user.id if bd_user else None,
            company_raw_id=company_raw.id,
            status=row.get("類型"),
            note="; ".join(
                filter(None, [
                    str(row.get("性質") or "").strip(),
                    str(row.get("規模") or "").strip(),
                    str(row.get("融資階段") or "").strip(),
                ])
            ) or None,
            updated_at=datetime.strptime(row["最近編輯"], "%Y-%m-%d %H:%M") if row.get("最近編輯") else None,
            created_at=datetime.strptime(row["添加日期"], "%Y-%m-%d %H:%M") if row.get("添加日期") else None,
        )
        session.add(client)
        session.flush()  # 先拿到 client.id

        # 匯入行業 (client_industry)
        # industry_id = row.get("行業")
        # if industry_id:
        #     ci = ClientIndustry(
        #         client_id=client.id,
        #         industry_id=int(industry_id)
        #     )
        #     session.add(ci)

    session.commit()

    if rejected_rows:
        os.makedirs("output", exist_ok=True)
        pd.DataFrame(rejected_rows).to_csv(
            "output/rejected_clients.csv",
            index=False,
            encoding="utf-8-sig"
        )

    print("✅ Client 匯入完成")
