import pandas as pd
from datetime import datetime
from schema.talent import talent
from schema.company_raw import company_raw
from schema.users import users
from utils.schema_loader import build_dtype_from_schema

def run(input_path="input/candidate.csv", output_path="output/talent.csv"):
    dtype_map = build_dtype_from_schema(talent.columns)
    df = pd.read_csv(input_path, dtype=dtype_map, keep_default_na=False)

    for _, row in df.iterrows():
        try:
            # 找到擁有者
            owner_name = str(row["擁有者"]).strip()
            user_row = next((u for u in users.rows if u["name"].strip() == owner_name), None)
            if not user_row:
                print(f"⚠️ User not found for {owner_name}, skip {row['EID']}")
                continue

            # 找到公司
            company_name_raw = row.get("公司")
            company_name_str = str(company_name_raw).strip().lower()
            
            print(company_name_str)

            if company_name_raw is None or company_name_str in ["", "nan"]:
                company_row = None
            else:
                company_row = next((c for c in company_raw.rows if c["name"].strip() == str(company_name_raw).strip()), None)

            if company_row is None and company_name_str not in ["", "nan"]:
                raise ValueError(f"Company not found for {company_name_raw} (EID={row['EID']})")

            # 拆生日
            birth = str(row.get("生日", "")).strip()
            birth_year, birth_month, birth_day = None, None, None
            if birth and "-" in birth:
                parts = birth.split("-")
                if len(parts) == 3:
                    birth_year, birth_month, birth_day = map(int, parts)

            # 匯入 talent
            talent.insert(
                id=row["EID"],
                created_by_id=user_row["id"],
                source_id=1,  # 先固定為 import
                company_raw_id=company_row["id"] if company_row else None,
                current_title=row.get("職位"),
                status=row.get("狀態"),
                updated_at=row.get("最近操作", datetime.now()),
                current_salary=row.get("年薪"),
                phone_country_code=row.get("國碼"),
                phone_number=row.get("號碼"),
                phone_extension=row.get("分機"),
                email=row.get("郵箱"),
                created_at=row.get("添加日期", datetime.now()),
                cv_url=row.get("簡歷"),
                name_chinese=row.get("中文名"),
                name_english=row.get("英文名"),
                birth_year=birth_year,
                birth_month=birth_month,
                birth_day=birth_day,
                highest_education=row.get("學歷"),
                highest_school=row.get("學校"),
                highest_major=row.get("專業"),
                expected_salary_status=row.get("salary_status")
            )

        except ValueError as e:
            print("Error:", e)

    talent.export_csv(output_path)
    print(f"✅ Talent data exported to {output_path}")
