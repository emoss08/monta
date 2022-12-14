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

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from core.exceptions import AuthenticationError


@require_POST
@sensitive_post_parameters("password")
def monta_authenticate_user(request: ASGIRequest) -> JsonResponse:
    """
    Function to authenticate user.

    :param request: The request object
    :type request: ASGIRequest
    :return: The user object or None if the user does not exist
    :rtype: JsonResponse
    """
    try:
        username: str = request.POST["username"]
        password: str = request.POST["password"]
        user: AbstractBaseUser | None = authenticate(
            username=username, password=password
        )
        if user is not None and user.is_active:
            auth_login(request, user)
            return JsonResponse({"message": "User logged in successfully"}, status=200)
        return JsonResponse({"message": "Invalid username or password"}, status=400)

    except AuthenticationError as login_error:
        raise login_error


def monta_logout_user(request: ASGIRequest) -> HttpResponseRedirect | None:
    """
    Function to log out user.

    :param request: The request object
    :type request: ASGIRequest
    :return: The user object or None if the user does not exist
    :rtype: HttpResponseRedirect | None
    """
    try:
        auth_logout(request)
        return HttpResponseRedirect("/")
    except AuthenticationError:
        return None
