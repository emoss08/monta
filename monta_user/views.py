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

from typing import Any, Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.db.models import QuerySet
from django.http import (
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST, require_safe
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView, UpdateView
from django_extensions.auth.mixins import ModelUserFieldPermissionMixin

from monta_user import forms, models


@method_decorator(require_safe, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class UserProfileView(LoginRequiredMixin, ModelUserFieldPermissionMixin, ListView):
    """
    Class to render overview page for the user profile app.
    """

    model: Type[models.Profile] = models.Profile
    template_name: str = "user_profile/overview.html"
    model_permission_user_field: str = "user"

    def get_queryset(self) -> QuerySet[models.Profile]:
        """
        Method to get the queryset for the view.

        :return: Queryset for the view.
        :rtype: QuerySet[models.Profile]
        """
        queryset: QuerySet[models.Profile] = models.Profile.objects.filter(
            user=self.request.user
        ).select_related("user")
        return queryset


@method_decorator(require_safe, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class UserProfileSettings(LoginRequiredMixin, ModelUserFieldPermissionMixin, ListView):
    """
    Class to render settings page for the user profile app.
    """

    model: Type[models.Profile] = models.Profile
    template_name: str = "user_profile/settings.html"
    model_permission_user_field = "user"

    def get_queryset(self) -> QuerySet[models.Profile]:
        """
        Method to get the queryset for the view.

        :return: Queryset for the view.
        :rtype: QuerySet[models.Profile]
        """
        queryset: QuerySet[models.Profile] = models.Profile.objects.filter(
            user=self.request.user
        ).select_related("user")
        return queryset


@method_decorator(require_POST, name="dispatch")
class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    """
    Class to update user's general information.
    """

    model: Type[models.Profile] = models.Profile
    form_class: Type[
        forms.UpdateProfileGeneralInformationForm
    ] = forms.UpdateProfileGeneralInformationForm
    success_url: str = "/"

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Method to handle POST requests.

        :param request: Request object.
        :type request: ASGIRequest
        :param args: Arguments.
        :type args: list
        :param kwargs: Keyword arguments.
        :type kwargs: dict
        :return: Response object.
        :rtype: JsonResponse
        """
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"result": "success", "message": "Profile Updates Posted Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": form.errors},
            status=400,
        )


@method_decorator(require_POST, name="dispatch")
class UpdateUserEmail(LoginRequiredMixin, UpdateView):
    """
    Class to Update the user email action.
    """

    model: Type[models.MontaUser] = models.MontaUser
    form_class: Type[forms.UpdateUserEmailForm] = forms.UpdateUserEmailForm

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Method to handle POST requests.

        :param request: Request object.
        :type request: ASGIRequest
        :param args: Arguments.
        :type args: list
        :param kwargs: Keyword arguments.
        :type kwargs: dict
        :return: Response object.
        :rtype: JsonResponse
        """
        form: forms.UpdateUserEmailForm = self.form_class(
            data=request.POST, instance=self.get_object()
        )
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"result": "success", "message": "Email Updated Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": form.errors},
            status=400,
        )


@method_decorator(require_POST, name="dispatch")
@method_decorator(sensitive_post_parameters("password"), name="dispatch")
class UpdateUserPassword(LoginRequiredMixin, UpdateView):
    """
    Class to Update the user password action.
    """

    model: Type[models.MontaUser] = models.MontaUser
    form_class: Type[forms.UpdateUserPasswordForm] = forms.UpdateUserPasswordForm
    success_url: str = "/"

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Method to handle POST requests.

        :param request: Request object.
        :type request: ASGIRequest
        :param args: Arguments.
        :type args: Any
        :param kwargs: Keyword arguments.
        :type kwargs: Any
        :return: Response object.
        :rtype: JsonResponse
        """
        form: forms.UpdateUserPasswordForm = self.form_class(
            data=request.POST, instance=self.get_object()
        )
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"result": "success", "message": "Password Updated Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": form.errors},
            status=400,
        )
