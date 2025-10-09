from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class CustomException(HTTPException):
    def __init__(self, status_code: int, message: str, errors: list = None, code: str = None):
        self.status_code = status_code
        self.message = message
        self.errors = errors or []
        self.code = code

def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
            "code": exc.code
        }
    )