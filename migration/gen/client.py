import random
import pandas as pd
from datetime import datetime

# 你提供的 owners 名單
OWNERS = [
    "Dave 胡愷璇",
    "intern",
    "Jackson",
    "Lilian",
    "Michelle 高孟婕",
    "Randy",
    "Ryan",
    "Victoria"
]

def pick(prob, value):
    """以 prob 機率回傳 None，否則回傳 value"""
    return None if random.random() < prob else value

def generate_client_rows(candidate_companies):
    rows = []
    companies = list(candidate_companies)

    for company_name in companies:
        # 先決定 BD
        bd_value = pick(0.0969, random.choice(OWNERS))

        # status 邏輯
        if bd_value:
            status_value = random.choice(["open", "ongoing"])  # 有 BD → 非 None 且非 lead
        else:
            status_value = "lead"   # 沒有 BD → 一定是 lead


        row = {
            "公司名稱": pick(0.0, company_name),
            "城市": pick(0.7296, random.choice(["台北","新竹","台中","高雄","上海","東京"])),
            "行業": pick(0.6786, random.choice(["科技業","顧問","零售","醫美","消費品"])),
            "在職": pick(0.0, random.randint(10, 200)),
            "離職": pick(0.0, random.randint(0, 50)),
            "所有職缺": pick(0.0, random.randint(0, 20)),
            "類型": status_value,
            "BD": bd_value,
            "簡稱": pick(0.7704, company_name[:4]),
            "性質": pick(0.9133, random.choice(["外企辦事處","外商獨資","民營企業","國有企業"])),
            "規模": pick(0.9337, random.choice(["少於10人","50~100人","500人以上"])),
            "融資階段": pick(0.9847, random.choice(["尚未獲投","A輪","B輪"])),
            "最近編輯": pick(0.0, datetime(2026, 7, random.randint(1,28), 14, 38).strftime("%Y-%m-%d %H:%M")),
            "添加人": pick(0.0, random.choice(OWNERS)),
            "添加日期": pick(0.0, datetime(2026, 7, random.randint(1,28)).strftime("%Y-%m-%d %H:%M")),
        }
        rows.append(row)

    return rows

if __name__ == "__main__":
    # 直接讀取 candidate.csv，抓出公司欄位
    candidate_df = pd.read_csv("input/candidate.csv", encoding="utf-8-sig")
    candidate_companies = set(candidate_df["公司"].dropna())

    client_rows = generate_client_rows(list(candidate_companies)[:5])
    client_df = pd.DataFrame(client_rows)
    client_df.to_csv("input/client.csv", index=False, encoding="utf-8-sig")
    print("✅ client.csv 已生成，來源公司完全沿用 candidate.csv")
