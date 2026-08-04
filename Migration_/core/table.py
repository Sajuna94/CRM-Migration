import pandas as pd

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
        self.next_id = 1

    def insert(self, **kwargs):
        # 先把 NaN 統一轉成 None
        for k, v in kwargs.items():
            if v is None:
                continue
            if isinstance(v, float) and pd.isna(v):
                kwargs[k] = None
            elif isinstance(v, str):
                if v.strip().lower() == "nan" or v.strip() == "":
                    kwargs[k] = None

        row = {}

        for col_name, col in self.columns.items():
            # 自動生成 id
            if getattr(col, "pk", False) and getattr(col, "auto_increment", False):
                if kwargs.get(col_name) is None:
                    kwargs[col_name] = self.next_id
                    self.next_id += 1

            # default 處理
            value = kwargs.get(col_name, col.default() if callable(col.default) else col.default)

            # 型別轉換
            if col.python_type and value is not None:
                try:
                    value = col.python_type(value)
                except Exception:
                    raise ValueError(f"{self.name}.{col_name} cannot convert {value} to {col.python_type}")

            # not_null 檢查
            if col.not_null and value is None:
                raise ValueError(f"{self.name}.{col_name} cannot be NULL")

            # unique 檢查
            if col.unique and any(r[col_name] == value for r in self.rows):
                raise ValueError(f"{self.name}.{col_name} must be UNIQUE")

            # check 檢查
            if col.check and value is not None and not col.check(value):
                raise ValueError(f"{self.name}.{col_name} failed CHECK constraint")

            row[col_name] = value

        self.rows.append(row)
        return row

    def delete_all(self):
        self.rows.clear()
        self.next_id = 1

    def export_csv(self, filepath):
        import pandas as pd
        df = pd.DataFrame(self.rows)
        df.to_csv(filepath, index=False, encoding="utf-8")
        print(f"Exported {self.name} table to {filepath}")
