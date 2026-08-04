import unicodedata


def normalize_text(value):
    if not isinstance(value, str):
        return value

    return unicodedata.normalize("NFKC", value).strip()