def build_note_content(fields, row):
    contents = {
        field: row.get(field)
        for field in fields
    }

    return "\n".join(
        f"{key}: {value}"
        for key, value in contents.items()
        if value
    )