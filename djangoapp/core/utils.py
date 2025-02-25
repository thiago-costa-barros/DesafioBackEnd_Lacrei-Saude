from rest_framework import status


def ApiResponse(success: bool, status_code: int, message: str, payload=None, error=None):
    response = {
        "success": success,
        "statusCode": status_code,
        "message": message,
        "payload": payload
    }
    
    # Adiciona "error" apenas se success for False e remove o payload
    if not success and error is not None:
        response.pop("payload", None)
        response["error"] = error
    
    return response