import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

PIPELINE_STAGES = ["added", "II", "PS", "CI", "PF", "PO", "SW", "fail", "split"]
SEXES = ["男", "女"]


def pick(prob, value):
    return None if random.random() < prob else value


def generate_rows(order_ids, candidate_ids, owners):
    rows = []

    for order_id in order_ids:
        # 每個 order 隨機 1~3 位候選人
        sample_candidates = random.sample(
            candidate_ids,
            k=min(random.randint(1, 3), len(candidate_ids))
        )

        for candidate_id in sample_candidates:
            base_time = datetime(
                2026, 7,
                random.randint(1, 28),
                random.randint(9, 18),
                random.randint(0, 59)
            )

            stage = random.choice(PIPELINE_STAGES)

            created_time = (
                base_time if stage == "added"
                else base_time - timedelta(days=random.randint(1, 7))
            )

            row = {
                "職缺流程": stage,
                "用戶": random.choice(owners),
                "最近更新": base_time.strftime("%Y-%m-%d %H:%M"),
                "添加時間": created_time.strftime("%Y-%m-%d %H:%M"),
                "性別": pick(0.3, random.choice(SEXES)),
                "招募網站": pick(0.1, 1),  # talent_source.id，假設已存在 id=1
                "人才智慧行業": pick(0.5, random.choice(["科技業", "金融業", "醫療", "零售"])),
                "人才智慧職能": pick(0.5, random.choice(["工程", "產品", "行銷", "業務"])),
                "candidate_id": candidate_id,  # 來自 candidate.csv
                "order_id": order_id,            # 來自 joborder.csv
            }

            rows.append(row)

    return rows


if __name__ == "__main__":
    candidate_df = pd.read_csv("input/candidate.csv", encoding="utf-8-sig")
    joborder_df = pd.read_csv("input/joborder.csv", encoding="utf-8-sig")

    candidate_ids = candidate_df["EID"].dropna().astype(str).tolist()
    order_ids = joborder_df["ID"].dropna().tolist()

    owners = (
        candidate_df["擁有者"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    rows = generate_rows(order_ids, candidate_ids, owners)

    df = pd.DataFrame(rows)
    df.to_csv("input/jobsubmission.csv", index=False, encoding="utf-8-sig")

    print(f"✅ jobsubmission.csv 已生成，共 {len(df)} 筆")
