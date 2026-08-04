import random
import pandas as pd
from datetime import datetime

def pick(prob, value):
    return None if random.random() < prob else value

def generate_joborder_rows(clients, candidates, owners):
    rows = []
    for i, row_client in enumerate(clients, start=1001):
        company_name = row_client["公司名稱"]
        client_rid = row_client["index"] + 1  # 用 index 當 rid
        candidate_eid = random.choice(candidates)

        row = {
            "ID": pick(0.00, i),
            "職缺名稱": pick(0.00, random.choice(["後端工程師","數據分析師","產品經理","業務開發"])),
            "客戶": pick(0.00, company_name),
            "添加者": random.choice(owners),
            "最近操作": pick(0.00, datetime(2026,7,random.randint(1,28),10,30).strftime("%Y-%m-%d %H:%M")),
            "工作地點": pick(0.00, random.choice(["台北","新竹","台中","高雄","上海","東京"])),
            "優先級": pick(0.9435, random.choice(["高","普通","低"])),
            "狀態": pick(0.00, random.choice(["進展中","失敗的","暫停的","已取消","成功的"])),
            "招聘數量": pick(0.00, random.randint(1,10)),
            "年薪": pick(0.8306, f"{random.randint(50,200)}萬"),
            "行業": pick(0.00, random.choice(["科技業","顧問","零售","醫美","消費品"])),
            "職能": pick(0.00, random.choice(["工程","行銷","業務","顧問"])),
            "學歷": "",
            "首次開啟日期": pick(0.00, datetime(2026,7,random.randint(1,28)).strftime("%Y-%m-%d")),
            "添加時間": pick(0.00, datetime(2026,7,random.randint(1,28)).strftime("%Y-%m-%d %H:%M")),
            "client_rid": pick(0.00, client_rid),
            "candidate_id": pick(0.00, candidate_eid),
        }
        rows.append(row)
    return rows

if __name__ == "__main__":
    client_df = pd.read_csv("input/client.csv", encoding="utf-8-sig")
    candidate_df = pd.read_csv("input/candidate.csv", encoding="utf-8-sig")

    clients = client_df[["公司名稱"]].dropna().reset_index().to_dict("records")[:5]
    candidates = list(candidate_df.loc[candidate_df["類型"] == "聯繫人", "EID"].dropna())

    owners = (
        candidate_df["擁有者"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    joborder_rows = generate_joborder_rows(clients, candidates, owners)
    joborder_df = pd.DataFrame(joborder_rows)
    joborder_df.to_csv("input/joborder.csv", index=False, encoding="utf-8-sig")
    print("✅ joborder.csv 已生成，客戶來源 client['公司名稱']，client_rid 用 index，candidate_id 直接取 EID")
