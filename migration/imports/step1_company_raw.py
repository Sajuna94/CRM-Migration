import pandas as pd
from schema.company import CompanyRaw
from schema.users import Users
from pipeline.db import SessionLocal

def run(candidate_path="input/candidate.csv", client_path="input/client.csv"):
    session = SessionLocal()

    # 讀取 candidate / client
    df_candidate = pd.read_csv(candidate_path)
    df_client = pd.read_csv(client_path)

    # 建立集合避免重複公司
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
            user = session.query(Users).filter_by(name=created_by_name).first()
            if not user:
                print(f"⚠️ User not found for {created_by_name}, skip {company_name}")
                continue

            company = CompanyRaw(
                name=company_name,
                created_by_id=user.id,
                created_at=created_at,
                updated_at=created_at
            )
            session.add(company)
            seen_companies.add(company_name)

    # 處理 client → company_raw
    for _, row in df_client.iterrows():
        company_name = row.get("公司名稱")
        created_by_name = row.get("添加人")
        created_at = row.get("添加日期")

        if pd.isna(company_name) or company_name == "":
            continue

        if company_name not in seen_companies:
            user = session.query(Users).filter_by(name=created_by_name).first()
            if not user:
                print(f"⚠️ User not found for {created_by_name}, skip {company_name}")
                continue

            company = CompanyRaw(
                name=company_name,
                created_by_id=user.id,
                created_at=created_at,
                updated_at=created_at
            )
            session.add(company)
            seen_companies.add(company_name)

    session.commit()
    print("✅ company_raw 匯入完成")
