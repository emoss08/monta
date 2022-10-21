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

# Standard library imports
from __future__ import annotations
from typing import Type, Any

# Core Django Imports
from ajax_datatable import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_safe
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView, CreateView, DetailView

# Monta Imports
from monta_fleet import models, forms
from monta_driver.models import Driver


@method_decorator(require_safe, name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class FleetListView(LoginRequiredMixin, TemplateView):
    """ """

    template_name: str = "fleet/index.html"


class CreateFleet(LoginRequiredMixin, CreateView):
    """ """

    model: Type[models.Fleet] = models.Fleet
    form_class: Type[forms.AddFleetForm] = forms.AddFleetForm

    def post(
        self, request: ASGIRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse | None:
        """
        :param request
        :type request: ASGIRequest
        :param args
        :type args: Any
        :param kwargs
        :type kwargs: Any
        :return: JsonResponse
        :rtype: JsonResponse | None
        """
        form: forms.AddFleetForm = forms.AddFleetForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"result": "success", "message": "Driver Posted Successfully"},
                status=201,
            )


class FleetEditView(LoginRequiredMixin, DetailView):
    """
    Class to render the driver edit page.
    """

    model: Type[models.Fleet] = models.Fleet

    def get_queryset(self) -> QuerySet[models.Fleet]:
        return (
            super(FleetEditView, self)
            .get_queryset()
            .filter(
                pk__exact=self.kwargs["pk"],
                organization=self.request.user.profile.organization,
            )
            .select_related("profile")
        )


def fleet_by_manager(
    request: ASGIRequest, manager_id: int, fleet_id: int
) -> HttpResponse | JsonResponse:
    if request.user.id == manager_id:
        fleet: models.Fleet = models.Fleet.objects.get(
            pk__exact=fleet_id, manager_id__exact=manager_id
        )
        driver_fleet = Driver.objects.filter(
            fleet_id__exact=fleet_id, organization_id__exact=fleet.organization_id
        ).select_related("profile")
        return render(
            request,
            "",
            {
                "fleet": fleet,
                "driver_fleet": driver_fleet,
            },
        )
    return JsonResponse(
        {"result": "error", "message": "You are not authorized to view this page"},
        status=403,
    )


@login_required
def delete_fleet(request: ASGIRequest, fleet_id: int) -> JsonResponse:
    """
    :param request
    :type request: ASGIRequest
    :param fleet_id
    :type fleet_id: int
    :return: JsonResponse
    :rtype: JsonResponse
    """
    fleet: models.Fleet = models.Fleet.objects.get(pk__exact=fleet_id)
    fleet.delete()
    return JsonResponse(
        {"result": "success", "message": "Fleet Deleted Successfully"},
        status=200,
    )


class FleetOverviewList(AjaxDatatableView, LoginRequiredMixin):
    """
    Class to render the driver overview page.
    """

    model: Type[Driver] = models.Fleet
    title: str = "Fleet Table"
    initial_order: list[list[str]] = [["first_name", "desc"]]
    column_defs: list[dict[str, str | bool]] = [
        {
            "name": "name",
            "title": "name",
            "visible": False,
            "orderable": True,
            "searchable": True,
        },
        {
            "name": "fleet_id",
            "title": "Fleet ID",
            "placeholder": True,
            "visible": True,
            "searchable": False,
        },
        {
            "name": "driver_fleet",
            "title": "Assigned Drivers",
            "placeholder": True,
            "visible": True,
            "searchable": False,
        },
    ]
