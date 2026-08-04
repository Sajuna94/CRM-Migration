import pandas as pd
from schema.company_raw import company_raw
from schema.users import users

def run(candidate_path="input/candidate.csv", client_path="input/client.csv", output_path="output/company_raw.csv"):
    # 讀取 candidate / client
    df_candidate = pd.read_csv(candidate_path)
    df_client = pd.read_csv(client_path)

    # 建立一個集合避免重複公司
    seen_companies = set()

    # 處理 candidate → company_raw
    for _, row in df_candidate.iterrows():
        company_name = row.get("公司")
        created_by_name = row.get("擁有者")
        created_at = row.get("添加日期")

        if pd.isna(company_name) or company_name == "":
            continue

        if company_name not in seen_companies:
            # 找 user_id
            user_row = next((u for u in users.rows if u["name"] == created_by_name), None)
            if not user_row:
                print(f"⚠️ User not found for {created_by_name}, skip {company_name}")
                continue

            try:
                company_raw.insert(
                    name=company_name,
                    created_by_id=user_row["id"],
                    created_at=created_at,
                    updated_at=created_at
                )
                seen_companies.add(company_name)
            except ValueError as e:
                print("Error:", e)

    # 處理 client → company_raw
    for _, row in df_client.iterrows():
        company_name = row.get("公司名稱")
        created_by_name = row.get("添加人")
        created_at = row.get("添加日期")

        if pd.isna(company_name) or company_name == "":
            continue

        if company_name not in seen_companies:
            # 找 user_id
            user_row = next((u for u in users.rows if u["name"] == created_by_name), None)
            if not user_row:
                print(f"⚠️ User not found for {created_by_name}, skip {company_name}")
                continue

            try:
                company_raw.insert(
                    name=company_name,
                    created_by_id=user_row["id"],
                    created_at=created_at,
                    updated_at=created_at
                )
                seen_companies.add(company_name)
            except ValueError as e:
                print("Error:", e)

    # 匯出結果
    company_raw.export_csv(output_path)
    print(f"✅ CompanyRaw data exported to {output_path}")
