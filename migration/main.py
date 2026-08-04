import sys
from pipeline.db_manager import DatabaseManager
from pipeline import clean
from imports import step0_taxonomy, step1_company_raw, step2_client, step3_talent, step4_opportunity, step5_pipeline

def main():
    clean.clear()
    
    # print("=== CRM Migration Pipeline ===")
    manager = DatabaseManager()
    manager.run()

    print("▶ 執行 step...")
    
    step0_taxonomy.run()
    # 根據 candidate & client 初始化 company raw table
    step1_company_raw.run()
    
    # 匯入 client 資料
    step2_client.run()
    
    # 匯入 talent, talent_note table
    # 匯入 client_contact 並補充 client
    step3_talent.run()
    
    
    step4_opportunity.run()
    
    step5_pipeline.run()

    # 之後可以逐步加上其他流程，例如:
    # from pipeline import load_note
    # load_note.insert_note(...)

if __name__ == "__main__":
    sys.exit(main())
