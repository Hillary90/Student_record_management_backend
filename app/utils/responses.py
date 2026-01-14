def success(message, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error(message, status_code=400):
    return {
        "status": "error",
        "message": message
    }, status_code
