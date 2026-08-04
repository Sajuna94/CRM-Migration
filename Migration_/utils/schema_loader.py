def build_dtype_from_schema(columns):
    """
    根據 schema 自動生成 dtype dict
    - varchar / text / citext → str
    - 其他型別保持預設
    """
    dtype = {}
    for name, col in columns.items():
        if col.col_type.startswith("varchar") or col.col_type in ["text", "citext"]:
            dtype[name] = str
    return dtype
