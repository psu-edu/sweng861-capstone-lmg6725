def validate_response(data):

    if "choices" not in data:
        return False

    if not data["choices"]:
        return False

    return True