import json
from datetime import datetime

from schema.taxonomy import IndustryNode, FunctionNode
from pipeline.db import SessionLocal


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def insert_nodes(session, nodes, model, parent_id=None):
    for index, node in enumerate(nodes):
        item = model(
            parent_id=parent_id,
            name=node["title"],
            sort_order=index,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        session.add(item)
        session.flush()

        if "children" in node:
            insert_nodes(session, node["children"], model, item.id)


def run(industry_path="input/industry.json", function_path="input/function.json"):
    session = SessionLocal()

    industry_tree = load_json(industry_path)
    function_tree = load_json(function_path)

    try:
        insert_nodes(session, industry_tree, IndustryNode)
        insert_nodes(session, function_tree, FunctionNode)

        session.commit()
        print("✅ taxonomy 匯入完成")

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


if __name__ == "__main__":
    run()