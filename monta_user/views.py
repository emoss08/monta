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

# Standard Library Imports
from typing import Any, Type

# Core Django Imports
from django.views.generic import UpdateView, ListView
from django.db.models import QuerySet, Model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.http import (
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST, require_safe
from django.views.decorators.vary import vary_on_cookie

# Third Party Imports
from django_extensions.auth.mixins import ModelUserFieldPermissionMixin

# Core Monta Imports
from monta_user import models, forms


@method_decorator(require_safe, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class UserProfileView(LoginRequiredMixin, ModelUserFieldPermissionMixin, ListView):
    """
    Class to render overview page for the user profile app.

    Typical Usage:
        >>> UserProfileView.as_view()
    """

    model: Type[models.Profile] = models.Profile
    template_name = "user_profile/overview.html"
    model_permission_user_field = "user"

    def get_queryset(self) -> QuerySet[models.Profile]:
        """
        Method to get the queryset for the view.

        :return: Queryset for the view.
        :rtype: QuerySet[models.Profile]
        """
        return models.Profile.objects.filter(user=self.request.user).select_related(
            "user"
        )


@method_decorator(require_safe, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class UserProfileSettings(LoginRequiredMixin, ModelUserFieldPermissionMixin, ListView):
    """
    Class to render settings page for the user profile app.

    Typical usage example:
        >>> UserProfileSettings.as_view()
    """

    model: Type[models.Profile] = models.Profile
    template_name = "user_profile/settings.html"
    model_permission_user_field = "user"

    def get_queryset(self) -> QuerySet[models.Profile]:
        """
        Method to get the queryset for the view.

        :return: Queryset for the view.
        :rtype: QuerySet[models.Profile]
        """
        return models.Profile.objects.filter(user=self.request.user).select_related(
            "user"
        )


@method_decorator(require_POST, name="dispatch")
class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    """
    Class to update user's general information.

    Overwrite the default dispatch method to check if the user is authenticated, if the user is not
    authenticated, raise a PermissionDenied exception. After the user is authenticated, call the
    default dispatch method. After the default dispatch method is called, check if the request method
    is POST, if the request method is not POST, raise a PermissionDenied exception.

    Typical usage example:
        >>> UpdateUserProfile.as_view()
    """

    model: Type[models.Profile] = models.Profile
    form_class: Type[
        forms.UpdateProfileGeneralInformationForm
    ] = forms.UpdateProfileGeneralInformationForm
    success_url = "/"

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

    Overwrites the dispatch method to check if the password is correct. If the password is correct,
    the form_valid method is called. If the password is incorrect, a JsonResponse is returned with
    the error message.

    Typical usage example:
        >>> UpdateUserEmail.as_view()
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
        form: forms.UpdateUserEmailForm = self.form_class(data=request.POST, instance=self.get_object())
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

    Overwrites the default dispatch method to check if the user current password is correct.
    If the password is correct, the form is valid and the password is updated.
    If the password is incorrect, return a JsonResponse with the error message.

    Returns:
        HttpResponse

    Typical usage example:
        UpdateUserPassword(request, user_id)
    """

    model: Type[models.MontaUser] = models.MontaUser
    form_class: Type[forms.UpdateUserPasswordForm] = forms.UpdateUserPasswordForm
    success_url = "/"

    def dispatch(
        self,
        request: ASGIRequest,
        *args,
        **kwargs,
    ) -> None | JsonResponse:
        """
        Method to check if the user is authenticated, if the user is not authenticated, raise a

        Args:
            request (ASGIRequest): The request object.
            *args: Arguments.
            **kwargs: Keyword arguments.

        Returns:
            None | JsonResponse: None if the user is authenticated, JsonResponse if the user is not authenticated.

        """
        user = self.get_object()
        if check_password(request.POST["current_password"], user.password):
            super().dispatch(request, *args, **kwargs)
        return JsonResponse(
            {"status": "error", "message": "Please check your password."}, status=400
        )

    def form_valid(self, form: forms.UpdateProfileGeneralInformationForm) -> None:
        """
        Method to update the user password.

        Args:
            form (forms.UpdateProfileGeneralInformationForm): Form to update the user password.

        Returns:
            None
        """
        form.instance.user = self.request.user
        super().form_valid(form)
