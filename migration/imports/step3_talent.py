import pandas as pd
import uuid
from datetime import datetime
from schema.talent import Talent, TalentNote
from schema.users import Users
from schema.client import Client, ClientContact
from schema.company import CompanyRaw
from pipeline.db import SessionLocal
import os
import json

from utils.note import build_note_content

def run(candidate_path="input/candidate.csv"):
    session = SessionLocal()
    rejected_rows = []

    df = pd.read_csv(
        candidate_path, 
        dtype={
            "號碼": str,
            "國碼": str,
            "分機": str,
            "簡歷": str,
        },
        converters={
            "年薪": lambda x: int(float(x)) if x else None,
            "company_private": lambda x: x.strip().lower() == "true" if x else None,
        },
    )
    df = df.replace({pd.NA: None, float("nan"): None})
    
    eid_map = {}  # EID → UUID 對應表

    for _, row in df.iterrows():
        # ==========================
        # reject validation
        # ==========================

        if not row.get("中文名") and not row.get("英文名"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_name"
            rejected_rows.append(rejected)
            continue

        if not row.get("郵箱") and not row.get("號碼") and not row.get("簡歷"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_contact"
            rejected_rows.append(rejected)
            continue
        
        eid = str(row["EID"]).strip()
        if not eid: continue

        # 生成 UUID 並建立 mapping
        talent_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, eid))
        eid_map[eid] = talent_id

        # 找擁有者
        owner_name = str(row["擁有者"]).strip()
        user = session.query(Users).filter_by(name=owner_name).first()
        if not user:
            print(f"⚠️ User not found for {owner_name}, skip {eid}")
            continue

        # 找公司
        company_name = str(row["公司"]).strip()
        company = session.query(CompanyRaw).filter_by(name=company_name).first()

        # 拆生日
        birth = str(row.get("生日", "")).strip()
        birth_year, birth_month, birth_day = None, None, None
        if birth and "-" in birth:
            parts = birth.split("-")
            if len(parts) == 3:
                birth_year, birth_month, birth_day = map(int, parts)

        talent_updated_at = datetime.strptime(row["最近操作"], "%Y-%m-%d %H:%M") if row.get("最近操作") else None
        talent_created_at = datetime.strptime(row["添加日期"], "%Y-%m-%d %H:%M") if row.get("添加日期") else None

        # 匯入 talent
        talent = Talent(
            id=talent_id,
            created_by_id=user.id,
            source_id=1,
            company_raw_id=company.id if company else None,
            current_title=row.get("職位"),
            status=row.get("狀態"),
            updated_at=talent_updated_at,
            current_salary=row.get("年薪"),
            phone_country_code=row.get("國碼"),
            phone_number=row.get("號碼"),
            phone_extension=row.get("分機"),
            email=row.get("郵箱"),
            created_at=talent_created_at,
            cv_url=row.get("簡歷"),
            name_chinese=row.get("中文名"),
            name_english=row.get("英文名"),
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            highest_school=row.get("學校"),
            highest_education=row.get("學歷"),
            highest_major=row.get("專業"),
            company_confidential=row.get("company_private"),
            expected_salary_status=row.get("salary_status")
        )
        session.add(talent)

        # 匯入 notes
        note_content = row.get("備註內容")
        recent_noted_user = str(row.get("最近備註者")).strip()
        note_created_user = session.query(Users).filter_by(name=recent_noted_user).first()
        
        if note_content and not note_created_user:
            print(f"⚠️ Noted User not found for {recent_noted_user}, skip {eid}")
            continue
        
        if note_content:
            contact_time = datetime.strptime(row["最近聯繫"], "%Y-%m-%d %H:%M") if row.get("添加日期") else None
            
            
            note = TalentNote(
                talent_id=talent_id,
                created_by_id=note_created_user.id,
                content=note_content,
                created_at=contact_time,
                updated_at=contact_time
            )
            session.add(note)
            
        # 匯入 talent_note(1)
        note_content = build_note_content([
            "地區",
            "工作年限",
            "意圖地區",
            "薪資結構",
            "期望薪資",
            "地址"
        ], row)

        if note_content:
            note = TalentNote(
                talent_id=talent_id,
                created_by_id=user.id,
                content=note_content,
                created_at=talent_created_at,
                updated_at=talent_created_at
            )
            session.add(note)
            
        
            
        # ==========================
        # Step 2: 如果是聯繫人 → 建立 ClientContact
        # ==========================
        candidate_type = str(row.get("類型") or "").strip()
        if candidate_type == "聯繫人":
            # 找 client by company_raw
            client = None
            if company:
                client = session.query(Client).filter_by(company_raw_id=company.id).first()

            # 如果沒有 client → 建立一個新的
            if not client and company:
                client = Client(
                    created_by_id=user.id,
                    company_raw_id=company.id,
                    status="lead",  # 預設狀態，可依需求調整
                    note="auto-created from contact",
                    created_at=talent_created_at,
                    updated_at=talent_created_at
                )
                session.add(client)
                session.flush()

            # 建立 client_contact
            if client:
                if row["EID"] == "EID-0001":
                    print("insert EID")
                contact = ClientContact(
                    client_id=client.id,
                    talent_id=talent.id,
                    created_by_id=user.id,
                    created_at=talent_created_at,
                    updated_at=talent_created_at
                )
                session.add(contact)
                     

    session.commit()
    
    if rejected_rows:
        os.makedirs("output", exist_ok=True)

        pd.DataFrame(rejected_rows).to_csv(
            "output/rejected_candidates.csv",
            index=False,
            encoding="utf-8-sig"
        )
    
    print("✅ Talent 匯入完成")
