from imports.steps import step1_users, step2_company_raw, step3_talent, step4_client

def main():
    # Step1: 匯入 users
    step1_users.run()
    step2_company_raw.run()
    step3_talent.run()
    # step4_client.run_client()

    # 未來可以加更多 step
    # step2_orders.run()
    # step3_relations.run()

if __name__ == "__main__":
    main()
