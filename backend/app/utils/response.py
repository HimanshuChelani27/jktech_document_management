def make_response(data, code=200, message=None):
    response = {
        "code": code,
        "details": data
    }
    if message:
        response["message"] = message
    return response
