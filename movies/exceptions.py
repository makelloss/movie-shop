from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler


class Conflict(APIException):
    """409: запит коректний, але суперечить поточному стану даних."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Операцію неможливо виконати через конфлікт даних."
    default_code = "conflict"


def custom_exception_handler(exc, context):
    """Єдиний формат помилок: {"error": {"status", "message", "details"}}"""
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        message = "Надіслано невалідні дані. Виправте поля, вказані в details."
        details = response.data
    else:
        data = response.data
        message = data.get("detail", str(exc)) if isinstance(data, dict) else str(exc)
        details = None

    response.data = {
        "error": {
            "status": response.status_code,
            "message": str(message),
            "details": details,
        }
    }
    return response