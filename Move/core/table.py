class Table:

    def __init__(self, name, columns, primary_key=None, unique=None, foreign_keys=None, checks=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique = unique or []
        self.foreign_keys = foreign_keys or {}
        self.checks = checks or []

        self.rows = []
        self.pk_index = set()
        self.unique_indexes = {fields: {} for fields in self.unique}


    def insert(self, row):
        if self.primary_key and self.primary_key not in row:
            row[self.primary_key] = len(self.rows) + 1
            
        if set(row.keys()) != set(self.columns):
            raise ValueError(f"{self.name}: column mismatch")

        if self.primary_key:
            pk = row[self.primary_key]

            if pk in self.pk_index:
                raise ValueError(f"{self.name}: duplicate primary key {pk}")

        for fields in self.unique:
            key = tuple(row[field] for field in fields)

            if key in self.unique_indexes[fields]:
                raise ValueError(f"{self.name}: duplicate unique {key}")

        for column, reference in self.foreign_keys.items():
            value = row[column]

            if value is not None and reference.find_by_pk(value) is None:
                raise ValueError(f"{self.name}: foreign key violation {column}={value}")

        for check in self.checks:
            if not check(row):
                raise ValueError(f"{self.name}: check constraint failed")


        self.rows.append(row)

        if self.primary_key:
            self.pk_index.add(row[self.primary_key])

        for fields in self.unique:
            key = tuple(row[field] for field in fields)
            self.unique_indexes[fields][key] = row


    def find_by_pk(self, value):
        if not self.primary_key:
            return None

        for row in self.rows:
            if row[self.primary_key] == value:
                return row

        return None


    def find_by_unique(self, field, value):
        key = (field,)

        if key not in self.unique_indexes:
            raise ValueError(f"{self.name}: {field} is not unique")

        return self.unique_indexes[key].get((value,))


    def export_csv(self, path):
        import csv

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(self.rows)