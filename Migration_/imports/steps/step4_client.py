import pandas as pd
from schema.client import client
from utils.schema_loader import build_dtype_from_schema
from schema.users import users
from schema.company_raw import company_raw


def run_client(input_path="input/client.csv", output_path="output/client.csv"):
    dtype_map = build_dtype_from_schema(client.columns)
    df = pd.read_csv(input_path, dtype=dtype_map, keep_default_na=False)

    for _, row in df.iterrows():
        try:
            # 找到擁有者
            owner_name = str(row["添加人"]).strip()
            user_row = next((u for u in users.rows if u["name"].strip() == owner_name), None)
            if not user_row:
                print(f"⚠️ User not found for {owner_name}, skip {row['EID']}")
                continue
            
            # 處理 client id
            client_id = int(row["Client_id"][1:])

            # 找到 BD
            sales_owner_name = str(row.get("BD", "")).strip()
            sales_owner_row = next((u for u in users.rows if u["name"].strip() == sales_owner_name), None)

            # 找到公司
            company_name_raw = row.get("公司名稱")
            company_name_str = str(company_name_raw).strip().lower()

            if company_name_raw is None or company_name_str in ["", "nan"]:
                company_row = None
            else:
                company_row = next((c for c in company_raw.rows if c["name"].strip() == str(company_name_raw).strip()), None)

            if company_row is None and company_name_str not in ["", "nan"]:
                print(f"⚠️ Company not found for {company_name_raw}, skip {row['EID']}")
                continue

            # 匯入 client
            client.insert(
                id=client_id,
                created_by_id=user_row["id"],
                sales_owner_id=sales_owner_row["id"] if sales_owner_row else None,
                company_raw_id=company_row["id"] if company_row else None,
                status=row.get("類型"),   # mapping 到 client_status
                note=row.get("城市") or row.get("行業"),
                created_at=row.get("添加日期"),
                updated_at=row.get("最近操作")
            )

        except ValueError as e:
            print("Error:", e)

    client.export_csv(output_path)
    print(f"✅ Client data exported to {output_path}")
