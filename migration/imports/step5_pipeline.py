import os
import uuid
import pandas as pd
import json
from datetime import datetime

from pipeline.db import SessionLocal
from schema.users import Users
from schema.pipeline import Pipeline, PipelineStageHistory
from schema.opportunity import Opportunity
from schema.talent import Talent
from schema.note import Note, NoteTargetType

from utils.note import build_note_content
from utils.asc import normalize_text

STAGE_FLOW = [
    "added",
    "II",
    "PS",
    "CI",
    "PF",
    "PO",
    "SW",
]

FINAL_STAGES = [
    "fail",
    "split",
]

def get_stage_history(stage):
    if stage == "fail":
        return ["added", "fail"]

    if stage == "split":
        return STAGE_FLOW + ["split"]

    return STAGE_FLOW[:STAGE_FLOW.index(stage) + 1]

def run(jobsubmission_path="input/jobsubmission.csv"):
    session = SessionLocal()
    rejected_rows = []
    
    with open("mapping/opportunity_mapping.json", encoding="utf-8") as f:
        opportunity_mapping = json.load(f)

    df = pd.read_csv(jobsubmission_path).map(normalize_text)
    df = df.replace({pd.NA: None, float("nan"): None})

    for _, row in df.iterrows():

        # ==========================
        # basic validation
        # ==========================
        if not row.get("candidate_id"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_candidate_id"
            rejected_rows.append(rejected)
            continue

        if not row.get("order_id"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_order_id"
            rejected_rows.append(rejected)
            continue

        if not row.get("用戶"):
            rejected = row.to_dict()
            rejected["reason"] = "missing_user"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # find talent by EID
        # ==========================
        eid = str(row["candidate_id"]).strip()
        talent_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, eid)

        talent = session.query(Talent).filter_by(id=talent_uuid).first()
        if not talent:
            rejected = row.to_dict()
            rejected["reason"] = "talent_not_found"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # find opportunity by order_id
        # ==========================
        order_id = opportunity_mapping.get(str(row["order_id"]))
        opportunity = session.query(Opportunity).filter_by(id=order_id).first()

        if not opportunity:
            rejected = row.to_dict()
            rejected["reason"] = "opportunity_not_found"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # find user
        # ==========================
        user_name = str(row["用戶"]).strip()
        user = session.query(Users).filter_by(name=user_name).first()

        if not user:
            rejected = row.to_dict()
            rejected["reason"] = "user_not_found"
            rejected_rows.append(rejected)
            continue

        # ==========================
        # mapping stage
        # ==========================
        stage = row.get("職缺流程") or "added"

        # ==========================
        # parse datetime
        # ==========================
        stage_entered_at = (
            datetime.strptime(row["最近更新"], "%Y-%m-%d %H:%M")
            if row.get("最近更新")
            else None
        )

        added_time = (
            datetime.strptime(row["添加時間"], "%Y-%m-%d %H:%M")
            if row.get("添加時間")
            else None
        )

        # ==========================
        # upsert pipeline
        # ==========================
        pipeline = session.query(Pipeline).filter_by(
            opportunity_id=opportunity.id,
            talent_id=talent.id
        ).first()
        pipeline_time = added_time if stage == "added" else stage_entered_at

        if not pipeline:
            pipeline = Pipeline(
                opportunity_id=opportunity.id,
                talent_id=talent.id,
                owner_id=user.id,
                stage=stage,
                stage_entered_at=pipeline_time
            )
            session.add(pipeline)
        else:
            pipeline.owner_id = user.id
            pipeline.stage = stage
            pipeline.stage_entered_at = pipeline_time

        # ==========================
        # talent note (migration mapping -> note.content)
        # ==========================
        note_content = build_note_content([
            "人才智慧行業",
            "人才智慧職能",
        ], row)

        if note_content:
            note = Note(
                target_type=NoteTargetType.talent.value,
                target_id=str(talent.id),
                created_by_id=user.id,
                content=str(note_content),
                created_at=stage_entered_at,
                updated_at=stage_entered_at
            )
            session.add(note)

        # ==========================
        # pipeline history
        # ==========================
        for history_stage in get_stage_history(stage):
            history_created_at = (
                added_time
                if history_stage == "added"
                else stage_entered_at
            )

            history = PipelineStageHistory(
                opportunity_id=opportunity.id,
                talent_id=talent.id,
                changed_by_id=user.id,
                to_stage=history_stage,
                created_at=history_created_at
            )

            session.add(history)

    session.commit()

    if rejected_rows:
        os.makedirs("output", exist_ok=True)

        pd.DataFrame(rejected_rows).to_csv(
            "output/rejected_jobsubmission.csv",
            index=False,
            encoding="utf-8-sig"
        )

    print("✅ JobSubmission 匯入完成")
