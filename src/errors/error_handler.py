from src.errors.types_errors import HttpConflitError, HttpBadRequestError, HttpNotFoundError, HttpUnauthorized
from src.presentation.http_types.http_response import HttpResponse

def handle_errors(error: Exception) -> HttpResponse:
    if isinstance(error, (HttpConflitError, HttpBadRequestError, HttpNotFoundError, HttpUnauthorized)):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors" : [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )
    
    return HttpResponse(
        status_code=500,
        body={
            "errors" : [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )
