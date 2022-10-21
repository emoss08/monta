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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView

# Third Party Imports
from braces import views

# Monta Imports
from monta_locations import models, forms


class LocationListView(LoginRequiredMixin, views.PermissionRequiredMixin, TemplateView):
    """
    Class to render the driver Index page.
    """

    template_name: str = "monta_location/index.html"
    permission_required: str = "monta_driver.view_driver"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Method to get the context data for the driver index page.

        :param kwargs: Keyword arguments.
        :type kwargs: Any
        :return: Returns the context data for the driver index page.
        :rtype: dict[str, Any]
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["fleets"] = models.Location.objects.filter(
            organization=self.request.user.profile.organization
        )
        context["location_form"]: forms.AddLocationForm = forms.AddLocationForm()
        return context


class LocationCreateView(LoginRequiredMixin, views.PermissionRequiredMixin, CreateView):
    """
    Class to create a new location.
    """

    model: Type[models.Location] = models.Location
    form_class: Type[forms.AddLocationForm] = forms.AddLocationForm
    permission_required: str = "monta_location.add_location"

    @transaction.atomic
    def post(
        self,
        request: ASGIRequest,
        *args: Any,
        **kwargs: Any,
    ) -> JsonResponse:
        """
        Method to handle the POST request.

        :param request: The request object.
        :type request: ASGIRequest
        :param args: Any arguments.
        :type args: Any
        :param kwargs: Any keyword arguments.
        :type kwargs: Any
        :return: Returns a JSON response with a success value of True or False.
        :rtype: JsonResponse
        """
        add_location: forms.AddLocationForm = self.form_class(data=request.POST)
        if add_location.is_valid():
            add_location.save()
            return JsonResponse(
                {"result": "success", "message": "Location Posted Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": add_location.errors},
            status=400,
        )


class LocationUpdateView(LoginRequiredMixin, views.PermissionRequiredMixin, UpdateView):
    """
    Class to update a location.
    """

    model: Type[models.Location] = models.Location
    form_class: Type[forms.UpdateLocationForm] = forms.UpdateLocationForm
    permission_required: str = "monta_location.change_location"

    @transaction.atomic
    def post(
        self,
        request: ASGIRequest,
        *args: Any,
        **kwargs: Any,
    ) -> JsonResponse:
        """
        Overwrites the post method to check if the form is valid. If the form is valid, request the user's organization
        and save the form. If the form is not valid, return a JSON response with a success value of False.

        :param request: The request object.
        :type request: ASGIRequest
        :param args: Any arguments.
        :type args: Any
        :param kwargs: Any keyword arguments.
        :type kwargs: Any
        :return: Returns a JSON response with a success value of True or False.
        :rtype: JsonResponse
        """
        form: forms.UpdateLocationForm = self.form_class(data=request.POST)
        if form.is_valid():
            form.save(location=self.get_object())
            return JsonResponse(
                {"result": "success", "message": "Driver Posted Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": form.errors},
            status=400,
        )
