class Column:
    def __init__(self, col_type, pk=False, auto_increment=False,
                 not_null=False, unique=False, default=None, check=None):
        self.col_type = col_type
        self.pk = pk
        self.auto_increment = auto_increment
        self.not_null = not_null
        self.unique = unique
        self.default = default
        self.check = check

        # 自動解析 varchar(n)
        self.max_length = None
        self.python_type = None

        if col_type.startswith("varchar"):
            import re
            match = re.search(r"varchar\((\d+)\)", col_type)
            if match:
                self.max_length = int(match.group(1))
            self.python_type = str  # varchar 永遠是字串

        elif col_type in ["text", "citext"]:
            self.python_type = str
        elif col_type in ["integer", "smallint"]:
            self.python_type = int
