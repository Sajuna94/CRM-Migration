import os
import shutil


def clear():
    for folder in ["output", "mapping"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            os.makedirs(folder)

    print("✅ output/ mapping/ 已清空")