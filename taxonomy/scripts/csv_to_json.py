import csv
import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TAXONOMY_DIR = os.path.join(BASE_DIR, "seeds")

FILES = [
    "industry",
    "function"
]


def insert_node(parent, title):
    children = parent.setdefault("children", [])

    for child in children:
        if child["title"] == title:
            return child

    node = {
        "title": title
    }

    children.append(node)

    return node


def csv_to_tree(csv_file):
    root = []

    df = pd.read_csv(csv_file).fillna("")
    df = df[df.apply(lambda row: any(row.astype(str).str.strip()), axis=1)]

    levels = len(df.columns)

    parents = [None] * levels

    for _, row in df.iterrows():
        for depth, title in enumerate(row.tolist()[:levels]):
            title = str(title).strip()

            if not title:
                continue

            if depth == 0:
                node = next(
                    (item for item in root if item["title"] == title),
                    None
                )

                if node is None:
                    node = {"title": title}
                    root.append(node)

            else:
                node = insert_node(parents[depth - 1], title)

            parents[depth] = node

            # 清除更深層的舊 parent
            for i in range(depth + 1, levels):
                parents[i] = None

    return root


def export_json(name):
    csv_file = os.path.join(TAXONOMY_DIR, f"{name}.csv")
    json_file = os.path.join(TAXONOMY_DIR, f"{name}.json")

    tree = csv_to_tree(csv_file)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(
            tree,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Exported: {json_file}")


def main():
    for name in FILES:
        export_json(name)


if __name__ == "__main__":
    main()