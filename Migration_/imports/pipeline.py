from imports.steps import step1_users, step2_company_raw

class ImportPipeline:
    def __init__(self, source_csv, target_table):
        self.source_csv = source_csv
        self.target_table = target_table

    def run(self):
        step1_users.run()
        step2_company_raw()
        # df = step1_extract.run(self.source_csv)
        # df = step2_transform.run(df)
        # step3_validate.run(df, self.target_table)
        # step4_load.run(df, self.target_table)
