def require_fields(data, fields):
    """
    Check for missing required fields in request data.
    Returns a list of missing fields.
    """
    if not data:
        return fields

    missing = [field for field in fields if field not in data]
    return missing
