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

# If you use anything less than python 3.11 you will have to change
# the import to >>> from typing import Any, Type

from typing import Any, Type

from braces import views
from django.contrib.auth import mixins
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.asgi import ASGIRequest
from django.db.models import Model, QuerySet
from django.forms import Form
from django.forms.forms import BaseForm
from django.forms.models import ModelForm
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic

from core.generic import (
    MontaGenericCreateView,
    MontaGenericDeleteView,
    MontaGenericDetailView,
    MontaGenericTemplateView,
    MontaGenericUpdateView,
)


class MontaTemplateView(MontaGenericTemplateView):
    """
    A view that renders a template.
    """

    permission_required: str
    context_data: dict[str, Any] | None = None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Get the context for this view.
        :param kwargs: Any keyword arguments.
        :type kwargs: Any
        :return: A dictionary of context data.
        """
        context: dict[str, Any] = self.context_data or {}
        if context:
            context.update(kwargs)
        else:
            context = kwargs
        return super().get_context_data(**context)


class MontaCreateView(MontaGenericCreateView):
    """
    View for creating a new object, with a Json response.
    """

    append_organization: bool = True

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        form: ModelForm[Model] = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if self.append_organization:
                form.instance.organization = self.request.user.profile.organization
            form.save()
            return JsonResponse(
                {
                    "result": "success",
                    "message": "New Record Created Successfully!",
                },
                status=201,
            )
        return JsonResponse(
            {
                "result": "error",
                "message": form.errors,
            },
            status=400,
        )


class MontaUpdateView(MontaGenericUpdateView):
    """
    View for updating an object, with a Json response.
    """

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        form: ModelForm = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "result": "success",
                    "message": "Record Updated Successfully!",
                },
                status=200,
            )
        return JsonResponse(
            {
                "result": "error",
                "message": form.errors,
            },
            status=400,
        )


class MontaDetailView(MontaGenericDetailView):
    """
    View for displaying an object, return a queryset.
    """

    filter_organization: bool = True
    select_related: bool = False
    select_related_fields: list[str] | tuple[str, ...]

    def get_queryset(self) -> QuerySet[Model]:
        """
        Method to get the queryset for the driver edit page.

        :return: The queryset for the driver edit page.
        :rtype: QuerySet | None
        """
        queryset: QuerySet[Any] = (
            super().get_queryset().filter(pk__exact=self.kwargs["pk"])
        )
        if self.filter_organization:
            queryset = queryset.filter(
                organization__exact=self.request.user.profile.organization
            )
        if self.select_related is not None:
            queryset = queryset.select_related(*self.select_related_fields)
        return queryset


class MontaDeleteView(MontaGenericDeleteView):
    """
    View for deleting an object, with a Json response.
    """

    form_class: None = None

    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:  # type: ignore
        """
        Handle DELETE requests: delete the object and return a JsonResponse.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        self.get_object().delete()
        return JsonResponse(
            {
                "result": "success",
                "message": "Record Deleted Successfully!",
            },
            status=204,
        )


class MontaSearchView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    """
    View for searching an object, with a template response
    """

    permission_required: str
    template_name: str
    model: Type[Model]
    form_class: Type[Form]
    search_vector: str
    filter_organization: bool

    def __init__(self) -> None:
        """
        If the form class is not an instance of ModelForm, raise an exception.
        """
        super().__init__()
        if self.form_class is not None:
            if not issubclass(self.form_class, BaseForm):
                raise ImproperlyConfigured(
                    "MontaSearchView.form_class must be a subclass of BaseForm."
                )

    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore
        """
        Handle GET requests: search the object and return a HttpResponse.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A HttpResponse
        """
        query = request.GET["query"] if "query" in request.GET else None
        form: Form = self.form_class(request.GET)
        results: QuerySet[Model] = self.model.objects.none()
        if query:
            form: Form = self.form_class({"query": query})
            search_query: SearchQuery = SearchQuery(query)
            if self.filter_organization:
                results: QuerySet[Model] = (
                    self.model.objects.annotate(
                        search=self.search_vector,
                        rank=SearchRank(self.search_vector, search_query),
                    )
                    .filter(
                        search=search_query,
                        organization=self.request.user.profile.organization,
                    )
                    .order_by("-rank")
                )
            else:
                results: QuerySet[Model] = (
                    self.model.objects.annotate(
                        search=self.search_vector,
                        rank=SearchRank(self.search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "query": query,
                "results": results,
            },
        )
