import os
import pandas as pd
import json
from datetime import datetime
import uuid

from schema.opportunity import Opportunity
from schema.client import ClientContact
from schema.users import Users
from schema.note import Note, NoteTargetType
from schema.taxonomy import IndustryNode, FunctionNode
from schema.opportunity import OpportunityIndustry, OpportunityFunction
from pipeline.db import SessionLocal

from utils.asc import normalize_text
from utils.note import build_note_content


STATUS_MAP = {
    "進展中": "ongoing",
    "失敗的": "failed",
    "成功的": "placed",
    "暫停的": "pending",
}


def run(joborder_path="input/joborder.csv"):
    session = SessionLocal()
    rejected_rows = []
    opportunity_mapping = {}
    
    industry_map = {
        node.name: node.id
        for node in session.query(IndustryNode).all()
    }

    function_map = {
        node.name: node.id
        for node in session.query(FunctionNode).all()
    }

    df = pd.read_csv(
        joborder_path,
        dtype={
            "招聘數量": "Int64",
            "client_rid": int,
        },
    ).map(normalize_text)

    df = df.replace({pd.NA: None, float("nan"): None})

    for _, row in df.iterrows():

        # ==========================
        # reject validation
        # ==========================

        if not row.get("職缺名稱"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_title"
            rejected_rows.append(rejected)
            continue

        if not row.get("client_rid"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_client"
            rejected_rows.append(rejected)
            continue

        if not row.get("candidate_id"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_candidate"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # find client contact
        # ==========================

        talent_id = uuid.uuid5(
            uuid.NAMESPACE_DNS,
            str(row["candidate_id"]).strip()
        )

        contact = session.query(ClientContact).filter_by(
            talent_id=talent_id
        ).first()

        if not contact:
            rejected = row.to_dict()
            rejected["reason"] = "client_contact_not_found"
            rejected_rows.append(rejected)
            continue
        
        # ==========================
        # find user
        # ==========================
        user_name = str(row["添加者"]).strip()
        user = session.query(Users).filter_by(name=user_name).first()

        if not user:
            rejected = row.to_dict()
            rejected["reason"] = "user_not_found"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # parse datetime
        # ==========================

        opened_at = (
            datetime.strptime(row["首次開啟日期"], "%Y-%m-%d")
            if row.get("首次開啟日期")
            else None
        )

        created_at = (
            datetime.strptime(row["添加時間"], "%Y-%m-%d %H:%M")
            if row.get("添加時間")
            else None
        )


        # ==========================
        # mapping
        # ==========================

        priority = row.get("優先級") == "高"

        status = STATUS_MAP.get(
            row.get("狀態"),
            "ongoing"
        )


        # ==========================
        # create opportunity
        # ==========================

        opportunity = Opportunity(
            created_by_id=user.id,
            
            client_id=row.get("client_rid"),
            client_contact_id=contact.id,

            title=row.get("職缺名稱"),
            location=row.get("工作地點"),

            description="auto-imported",

            headcount=row.get("招聘數量"),

            status=status,
            is_priority=priority,

            opened_at=opened_at,

            note=row.get("年薪"),

            created_at=created_at,
            updated_at=created_at,
        )

        session.add(opportunity)
        session.flush()
        
        opportunity_mapping[str(row["ID"])] = opportunity.id
        
        note_content = build_note_content(["年薪"], row)
        if note_content:
            session.add(Note(
                target_type=NoteTargetType.opportunity.value,
                target_id=opportunity.id,
                created_by_id=user.id,
                content=note_content,
                created_at=created_at,
                updated_at=created_at,
            ))
            
        # ==========================
        # taxonomy mapping
        # ==========================

        for industry in str(row.get("行業")).split(","):
            industry = industry.strip()

            if not industry:
                continue

            industry_id = industry_map.get(industry)

            if not industry_id:
                rejected = row.to_dict()
                rejected["reason"] = "industry_not_found"
                rejected["value"] = industry
                rejected_rows.append(rejected)

                print(f"⚠️ Industry not found: {industry}")
                continue

            session.add(
                OpportunityIndustry(
                    opportunity_id=opportunity.id,
                    industry_id=industry_id
                )
            )


        for function in str(row.get("職能")).split(","):
            function = function.strip()

            if not function:
                continue

            function_id = function_map.get(function)

            if not function_id:
                rejected = row.to_dict()
                rejected["reason"] = "function_not_found"
                rejected["value"] = function
                rejected_rows.append(rejected)

                print(f"⚠️ Function not found: {function}")
                continue

            session.add(
                OpportunityFunction(
                    opportunity_id=opportunity.id,
                    function_id=function_id
                )
            )

    session.commit()
    
    with open("mapping/opportunity_mapping.json", "w", encoding="utf-8") as f:
        json.dump(opportunity_mapping, f, ensure_ascii=False, indent=2)

    # ==========================
    # export rejected
    # ==========================

    if rejected_rows:
        os.makedirs("output", exist_ok=True)

        pd.DataFrame(rejected_rows).to_csv(
            "output/rejected_joborders.csv",
            index=False,
            encoding="utf-8-sig"
        )


    print("✅ Opportunity 匯入完成")