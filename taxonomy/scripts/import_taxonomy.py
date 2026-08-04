import csv
import json
import sys
from pathlib import Path


def insert_node(parent, title):
    """
    在 children 中尋找相同 title，
    沒有則建立新的 node
    """
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

    with open(csv_file, encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        headers = next(reader)

        levels = len(headers)

        for row in reader:
            if not any(row):
                continue

            current = None

            for depth in range(levels):
                title = row[depth].strip()

                if not title:
                    continue

                if depth == 0:
                    children = root

                    node = None

                    for item in children:
                        if item["title"] == title:
                            node = item
                            break

                    if node is None:
                        node = {
                            "title": title
                        }
                        children.append(node)

                else:
                    node = insert_node(node, title)

    return root


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python import_taxonomy.py input.csv output.json"
        )
        return

    csv_file = Path(sys.argv[1])
    json_file = Path(sys.argv[2])

    tree = csv_to_tree(csv_file)

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            tree,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Exported: {json_file}")


if __name__ == "__main__":
    main()