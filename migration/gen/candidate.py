import random
import pandas as pd
from datetime import datetime

random.seed(42)

COMPANIES = ["Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", "Tesla", "IBM", "Intel", "Oracle"]
NAMES = [
    ("王小明", "Michael Wang"),
    ("李佳恩", "Jane Li"),
    ("陳志豪", "Kevin Chen"),
    ("林雅婷", "Emily Lin"),
    ("張家豪", "David Chang"),
    ("黃怡君", "Ivy Huang"),
    ("周柏霖", "Brian Chou"),
    ("吳欣怡", "Cindy Wu"),
]
POSITIONS = ["軟體工程師", "產品經理", "設計師", "行銷專員", "資料科學家"]
LOCATIONS = ["台北", "新竹", "台中", "高雄"]
OWNERS = ["Ryan", "Victoria", "Jackson", "Michelle 高孟婕", "Randy"]

def pick(prob, value):
    """以 prob 機率回傳 None，否則回傳 value"""
    return None if random.random() < prob else value

def random_phone():
    return "9" + "".join([str(random.randint(0,9)) for _ in range(8)])

def random_email(name_en, company, phone):
    prefix = name_en.lower().replace(" ", ".")
    return f"{prefix}.{phone}@{company.lower()}.com"

def generate_rows(n=8):
    rows = []
    used_keys = set()
    used_companies = set()

    for i in range(n):
        cn_name, en_name = random.choice(NAMES)
        company = random.choice(COMPANIES)
        used_companies.add(company)

        phone = random_phone()
        email = random_email(en_name, company, phone)

        while (email, phone) in used_keys:
            phone = random_phone()
            email = random_email(en_name, company)
        used_keys.add((email, phone))
        
        # 生成一個基準日期
        base_day = random.randint(1, 28)
        contact_time = datetime(2026, 7, base_day, 10, 30)
        operation_time = datetime(2026, 7, base_day, 14, 38)

        # 先決定最近備註者
        recent_noted_user = pick(0.5046, random.choice(OWNERS))

        # 如果有最近備註者，才可能有備註內容
        note_content = None
        if recent_noted_user:
            note_content = pick(0.5132, "這是備註內容")
            
        row = {
            "EID": pick(0.0, f"EID-{i+1:04d}"),
            "姓名": pick(0.0, cn_name),
            "公司": pick(0.0387, company),
            "職位": pick(0.0349, random.choice(POSITIONS)),
            "地區": pick(0.3197, random.choice(LOCATIONS)),
            "狀態": pick(0.0, random.choice(["active", "open", "hired", "unknown"])),
            "擁有者": pick(0.0005, random.choice(OWNERS)),
            "備註": pick(0.0, "測試備註"),
            "最近聯繫": pick(0.0002, datetime(2026, 7, random.randint(1,28), 10, 30).strftime("%Y-%m-%d %H:%M")),
            "最近備註者": recent_noted_user,
            "類型": pick(0.0002, random.choice(["聯繫人", "候選人"])),
            "最近操作": pick(0.0005, contact_time).strftime("%Y-%m-%d %H:%M"),
            "附件": pick(0.0005, "resume.pdf"),
            "社交主頁": None,
            "備註內容": note_content,
            "年薪": pick(0.9859, random.choice([1800000,2000000,2200000])),
            "工作年限": pick(0.0005, random.randint(2,10)),
            "號碼": pick(0.4341, phone),
            "郵箱": pick(0.3450, email),
            "標簽": None,
            "行業": pick(0.4888, "科技業"),
            "職能": pick(0.4964, random.choice(["工程","產品","設計","行銷","數據"])),
            "意圖地區": pick(0.5959, random.choice(LOCATIONS)),
            "學校": pick(0.1278, random.choice(["國立台灣大學","清華大學","交通大學"])),
            "學歷": pick(0.1559, random.choice(["bachelor","master"])),
            "專業": pick(0.1942, random.choice(["資訊工程","企業管理","工業設計"])),
            "添加人": pick(0.0002, random.choice(OWNERS)),
            "添加日期": pick(0.0005, operation_time).strftime("%Y-%m-%d %H:%M"),
            "簡歷": pick(0.0661, str(1000+i)),
            "中文名": pick(0.3614, cn_name),
            "國碼": pick(0.9155, "886"),
            "生日": pick(0.4426, f"199{random.randint(0,9)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"),
            "英文名": pick(0.3485, en_name),
            "薪資結構": pick(0.8644, random.choice(["年薪+股票","年薪+獎金"])),
            "期望薪資": pick(0.5424, f"年薪{random.choice([250,300,350])}萬"),
            "期望公司": None,
            "工作性質": None,
            "離職周期": None,
            "地址": pick(0.9599, f"{random.choice(LOCATIONS)}市XX區"),
            "推薦人": None,
            "分機": pick(0.7, "123"),
            "company_private": pick(0.0, "FALSE"),
            "salary_status": pick(0.0, random.choice(["negotiable","company_policy"])),
        }

        rows.append(row)
        
    return rows

if __name__ == "__main__":
    rows = generate_rows(30)
    df = pd.DataFrame(rows)
    df.to_csv("input/candidate.csv", index=False, encoding="utf-8-sig")
    print("✅ candidate.csv 已生成")
