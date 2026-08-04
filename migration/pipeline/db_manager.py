from sqlalchemy import text
from pipeline.db import engine, SessionLocal
from schema.users import Users, UserRole
from schema.talent import TalentSource, TalentSourceType


class DatabaseManager:
    def __init__(self):
        self.session = SessionLocal()

    def clear_tables(self, *tables):
        if not tables:
            raise ValueError("請至少指定一個 table")
        table_list = ", ".join(tables)
        sql = f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE;"
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
        print(f"✅ 已清空: {table_list}")

    def init_users(self):
        initial_users = [
            {"name": "Dave 胡愷璇", "email": "dave@example.com", "role": UserRole.consultant},
            {"name": "intern", "email": "intern@example.com", "role": UserRole.manager},
            {"name": "Jackson", "email": "jackson@example.com", "role": UserRole.admin},
            {"name": "Lilian", "email": "lilian@example.com", "role": UserRole.consultant},
            {"name": "Michelle 高孟婕", "email": "michelle@example.com", "role": UserRole.manager},
            {"name": "Randy", "email": "randy@example.com", "role": UserRole.consultant},
            {"name": "Ryan", "email": "ryan@example.com", "role": UserRole.admin},
            {"name": "Victoria", "email": "victoria@example.com", "role": UserRole.consultant},
        ]
        for u in initial_users:
            user = Users(**u)
            self.session.add(user)
        self.session.commit()
        print("✅ users 初始化完成")
        
    def init_talent_source(self):
        source = TalentSource(type=TalentSourceType.import_.value, name="gllue")
        self.session.add(source)
        self.session.commit()
        print("✅ talent_source 初始化完成")
    

    def run(self):
        print("=== CRM Migration Pipeline ===")
        # 改成實際存在的表
        self.clear_tables(
            "users",
            "company_raw",
            "company",
            "company_alias",
            "industry_node",
            "function_node",
            "talent",
            "talent_source",
            "talent_note",
            "talent_industry",
            "talent_function",
            "talent_education",
            "client",
            "client_contact",
            "client_industry",
            "pipeline_stage_history",
            "opportunity",
            "opportunity_industry",
            "opportunity_function",
            "pipeline"
        )
        print("▶ 初始化...")
        self.init_users()
        self.init_talent_source()
        # 之後加上其他 init_xxx()
        
        
        
        