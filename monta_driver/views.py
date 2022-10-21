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
from typing import (
    List,
    Type,
    Any,
)

# Core Django Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.handlers.asgi import ASGIRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.http import (
    require_safe,
)
from django.views.decorators.vary import vary_on_cookie
from django.views import generic
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)

# Third Party Imports
from ajax_datatable import AjaxDatatableView
from braces import views

# Core Monta Imports
from monta_driver import models, forms


@method_decorator(require_safe, name="dispatch")
@method_decorator(cache_control(max_age=60 * 60 * 24), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class DriverListView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    """
    Class to render the driver Index page.
    """

    template_name = "monta_driver/index.html"
    permission_required = "monta_driver.view_driver"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Method to get the context data for the driver index page.

        :param kwargs: Any keyword arguments.
        :type kwargs: Any
        :return: The context data for the driver index page.
        :rtype: dict[str, Any]
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["fleets"] = models.Fleet.objects.filter(
            organization=self.request.user.profile.organization
        ).order_by("id")
        context["create_driver_form"]: forms.AddDriverForm = forms.AddDriverForm()
        return context


class DriverCreateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.CreateView
):
    """
    Class to render create driver page.
    """

    model: Type[models.Driver] = models.Driver
    form_class: Type[forms.AddDriverForm] = forms.AddDriverForm
    permission_required = "monta_driver.add_driver"
    success_url = "/driver/"
    template_name = "monta_driver/index.html"

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
        :return: A JSON response with a success value of True or False.
        :rtype: JsonResponse
        """
        add_driver_form: forms.AddDriverForm = self.form_class(data=request.POST)
        contact_name: None = None
        contact_phone: None = None
        if add_driver_form.is_valid():
            driver = add_driver_form.save(commit=False)
            driver.organization = request.user.profile.organization
            driver.save()
            models.Driver.create_driver_profile(driver, **request.POST.dict())
            for key, val in {
                k_: v_
                for k_, v_ in request.POST.items()
                if k_.startswith("driver_list")
            }.items():
                if "contact_name" in key:
                    contact_name = val
                if "contact_phone" in key:
                    contact_phone = val
                models.DriverContact.objects.create(
                    driver=add_driver_form.instance,
                    contact_name=contact_name,
                    contact_phone=contact_phone,
                )
            return JsonResponse(
                {"result": "success", "message": "Driver Posted Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": add_driver_form.errors},
            status=400,
        )


@method_decorator(require_safe, name="dispatch")
class DriverEditView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DetailView
):
    """
    Class to render the driver edit page.
    """

    model: Type[models.Driver] = models.Driver
    template_name = "monta_driver/edit.html"
    permission_required = "monta_driver.change_driver"

    def get_queryset(self) -> QuerySet[models.Driver] | None:
        """
        Method to get the queryset for the driver edit page.

        :return: The queryset for the driver edit page.
        :rtype: QuerySet[models.Driver] | None
        """
        return (
            super(DriverEditView, self)
            .get_queryset()
            .filter(
                pk__exact=self.kwargs["pk"],
                organization=self.request.user.profile.organization,
            )
            .select_related("profile")
        )


class DriverUpdateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.UpdateView
):
    """
    Class to update the driver profile.
    """

    model: Type[models.Driver] = models.Driver
    form_class: Type[forms.UpdateDriverForm] = forms.UpdateDriverForm

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
        :return: A JSON response with a success value of True or False.
        :rtype: JsonResponse
        """
        form: forms.UpdateDriverForm = self.form_class(data=request.POST)
        if form.is_valid():
            form.save(driver=self.get_object())
            return JsonResponse(
                {"result": "success", "message": "Driver Posted Successfully"},
                status=201,
            )
        return JsonResponse(
            {"result": "error", "message": form.errors},
            status=400,
        )


class DriverDeleteView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DeleteView
):
    """
    Class to delete a driver.
    """

    model: Type[models.Driver] = models.Driver
    permission_required: str = "monta_driver.delete_driver"

    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Method to handle the GET request.

        :param request: The request object.
        :type request: ASGIRequest
        :param args: Any arguments.
        :type args: Any
        :param kwargs: Any keyword arguments.
        :type kwargs: Any
        :return: A JSON response with a success value.
        :rtype: JsonResponse
        """
        driver: models.Driver = self.get_object()
        driver.delete()
        return JsonResponse(
            {"result": "success", "message": "Driver Deleted Successfully"},
            status=204,
        )


class DriverOverviewList(mixins.LoginRequiredMixin, AjaxDatatableView):
    """
    Class to render the driver overview page.
    """

    model: Type[models.Driver] = models.Driver
    title: str = "Driver Table"
    initial_order: list[list[str]] = [["first_name", "desc"]]
    column_defs: list[dict[str, str | bool]] = [
        {
            "name": "first_name",
            "title": "name",
            "visible": False,
            "orderable": True,
            "searchable": True,
        },
        {
            "name": "information",
            "title": "Information",
            "placeholder": True,
            "visible": True,
            "searchable": False,
        },
        {
            "name": "license_number",
            "title": "License Number",
            "placeholder": True,
            "searchable": False,
            "className": "highlighted",
        },
        {
            "name": "license_state",
            "title": "License State",
            "visible": True,
            "searchable": False,
        },
        {
            "name": "license_expiration",
            "title": "License Expiration",
            "placeholder": True,
            "visible": True,
            "searchable": False,
        },
        {
            "name": "actions",
            "title": "Actions",
            "placeholder": True,
            "visible": True,
            "searchable": False,
            "className": "text-end",
        },
    ]

    def optimize_queryset(self, qs: QuerySet) -> QuerySet[models.Driver]:
        """
        Optimize the queryset by prefetching related objects.

        :param qs: The queryset to optimize.
        :type qs: QuerySet[models.Driver]
        :return: The optimized queryset.
        :rtype: QuerySet[models.Driver]
        """
        return qs.select_related("profile")

    def customize_row(self, row: dict, obj: models.Driver) -> dict:
        """
        Customize the row by adding the driver information, license number, license state, license expiration, and actions.

        :param row: The row to customize.
        :type row: dict
        :param obj: The driver object.
        :type obj: models.Driver
        :return: The customized row.
        :rtype: dict
        """
        row[
            "information"
        ] = f"""
            <div class="d-flex align-items-center">
            <div class="symbol symbol-45px me-5">
            <img src="{obj.profile.get_driver_profile_pic()}" alt="">
            </div>
            <div class="d-flex justify-content-start flex-column">
            <a href="#" class="text-dark fw-bold text-hover-primary fs-6">{obj.driver_id}</a>
            <span class="text-muted fw-semibold text-muted d-block fs-7">{obj.get_full_name}</span>
            </div>
            </div>"""
        row["license_number"] = f"{obj.profile.license_number}"
        row["license_state"] = f"{obj.profile.license_state}"
        row["license_expiration"] = f"{obj.profile.license_expiration}"
        row[
            "actions"
        ] = f"""
        <td class="text-end">
        <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M17.5 11H6.5C4 11 2 9 2 6.5C2 4 4 2 6.5 2H17.5C20 2 22 4 22 6.5C22 9 20 11 17.5 11ZM15 6.5C15 7.9 16.1
        9 17.5 9C18.9 9 20 7.9 20 6.5C20 5.1 18.9 4 17.5 4C16.1 4 15 5.1 15 6.5Z" fill="currentColor"></path>
        <path opacity="0.3" d="M17.5 22H6.5C4 22 2 20 2 17.5C2 15 4 13 6.5 13H17.5C20 13 22 15 22 17.5C22 20 20 22 17.5
        22ZM4 17.5C4 18.9 5.1 20 6.5 20C7.9 20 9 18.9 9 17.5C9 16.1 7.9 15 6.5 15C5.1 15 4 16.1 4 17.5Z"
        fill="currentColor"></path>
        </svg>
        </span>
        </a>
        <a href="{obj.get_absolute_url()}" class="btn btn-icon btn-bg-light
        btn-active-color-primary btn-sm me-1">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988
        17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355
        21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099
        14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449
        21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z"
        fill="currentColor"></path>
        <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744
        21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799
        20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z"
        fill="currentColor"></path>
        </svg>
        </span>
        </a>
        <a href="{reverse('driver_delete', kwargs={'pk': obj.id})}"
        class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm delete-record">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21
        5 19.6569 5 18V9Z" fill="currentColor"></path>
        <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18
        6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor"></path>
        <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor">
        </path>
        </svg>
        </span>
        </a>
        """
        return row


class DriverSearchView(mixins.LoginRequiredMixin, views.PermissionRequiredMixin, View):
    """
    Class to delete a driver.
    """

    permission_required: str = "monta_driver.search_drivers"

    def get(self, request: ASGIRequest) -> HttpResponse:
        """
        Get request for getting results from the search with params.

        :param request
        :type request: ASGIRequest
        :return HttpResponse of the Charge Type search form
        :rtype HttpResponse
        """
        form: forms.SearchForm = forms.SearchForm()
        query = request.GET["query"] if "query" in request.GET else None
        results: QuerySet[models.Driver] | list = []
        if query:
            form: forms.SearchForm = forms.SearchForm({"query": query})
            search_vector: SearchVector = SearchVector(
                "organization__name",
                "first_name",
                "last_name",
                "profile__license_state",
                "profile__license_number",
                "profile__license_expiration",
            )
            search_query: SearchQuery = SearchQuery(query)
            results: QuerySet[models.Driver] = (
                models.Driver.objects.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(
                    search=search_query, organization=request.user.profile.organization
                )
                .select_related("profile")
                .order_by("-rank")
            )
        return render(
            request,
            "monta_driver/search.html",
            {
                "form": form,
                "query": query,
                "results": results,
            },
        )


@login_required
@require_safe
def validate_license_number(request: ASGIRequest) -> HttpResponse:
    """
    Function to validate license number.

    If the license number is not already in use then return a success response. Otherwise, return an error response.

    **********************************************************************************************************************
    * NOTE: Ensure that you implement client side debouncing & Rate Limiting to prevent this function from being called
     on every keystroke *
    **********************************************************************************************************************

    :param request
    :type request: ASGIRequest
    :return HttpResponse
    :rtype HttpResponse
    """
    license_number: str | List[object] | None = (
        request.GET["license_number"] if "license_number" in request.GET else None
    )
    if license_number:
        form: forms.LicenseValidateForm = forms.LicenseValidateForm(
            {"license_number": license_number}
        )
        if form.is_valid():
            license_number: str | List[object] | None = form.cleaned_data[
                "license_number"
            ]
            if models.Driver.objects.filter(
                profile__license_number=license_number,
                organization=request.user.profile.organization,
            ).exists():
                return HttpResponse(
                    "<div class='text-danger ease_in_5' id='license_error'>License is already "
                    "taken.</div>"
                )
            return HttpResponse(
                "<div class='text-success ease_in_5' id='license_error'>License number is "
                "available.</div>"
            )
    else:
        return HttpResponse(
            "<div class='text-warning ease_in_5' id='license_error'>"
            "Enter a license number to check if it is available.</div>"
        )
