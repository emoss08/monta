# -*- coding: utf-8 -*-
"""
COPYRIGHT 2022 MONTA

This file is part of Monta.

Monta is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Monta is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Monta.  If not, see <https://www.gnu.org/licenses/>.
"""

from functools import wraps
from typing import Any, Callable, Type

from django.core.handlers.asgi import ASGIRequest
from django.db import models
from ninja.responses import Response


def check_organization(model: Type[models.Model]) -> Callable:
    """
    Decorator to check if the record belongs to user organization
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: ASGIRequest, *args: Any, **kwargs: Any) -> Response | Any:
            """
            Wrapper function

            :param request: ASGIRequest
            :type request: ASGIRequest
            :param args: Arguments
            :type args: Any
            :param kwargs: Keyword Arguments
            :type kwargs: Any
            """
            record = model.objects.get(id__exact=kwargs["id"])
            if record.organization != request.user.profile.organization:
                return Response(
                    {"error": "Record does not belong to your organization"},
                    status=403,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
