import pandas as pd
from datetime import datetime
from schema.users import users

def run(input_path="input/users.csv", output_path="output/users_clean.csv"):
    df = pd.read_csv(input_path)
    for _, row in df.iterrows():
        try:
            users.insert(
                name=row["name"],
                email=f"{row['name'].lower()}@example.com",
                role="consultant",
                status="active",
                create_at=datetime.now()
            )
        except ValueError as e:
            print("Error:", e)

    users.export_csv(output_path)
    print(f"✅ Users data imported and exported to {output_path}")
