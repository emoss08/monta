from functools import wraps
from typing import Type, Callable, Any
from django.core.handlers.asgi import ASGIRequest
from django.db import models
from ninja.responses import Response


def check_organization(model: Type[models.Model]) -> Callable:
    """
    Decorator to check if the record belongs to user organization
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: ASGIRequest, *args, **kwargs) -> Response | Any:
            """
            Wrapper function
            """
            record = model.objects.get(id=kwargs["id"])
            if record.organization != request.user.profile.organization:
                return Response(
                    {"error": "Record does not belong to your organization"},
                    status=403,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
