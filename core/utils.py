from rest_framework import status


def ApiResponse(sucess: bool, status_code: int, message: str, payload=None, error=None):
    response = {
        "success": sucess,
        "statusCode": status_code,
        "message": message,
        "payload": payload
    }
    
    # Adiciona "error" apenas se success for False
    if not sucess and error is not None:
        response["error"] = error
    
    return response