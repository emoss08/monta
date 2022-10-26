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
from typing import Any

from braces import views
from django.contrib.auth import mixins
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.handlers.asgi import ASGIRequest
from django.db.models import QuerySet
from django.db.models.base import Model
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic

from core import exceptions


# Monta Core views that can be used on any project to inherit from.


class MontaTemplateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    """
    A view that renders a template.
    """

    permission_required = None
    context_data = None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict = self.context_data or {}
        if context:
            context.update(kwargs)
        else:
            context: dict = kwargs
        return super().get_context_data(**context)


class MontaCreateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.CreateView
):
    """
    View for creating a new object, with a Json response.
    """

    permission_required = None
    form_class = None
    filter_organization: bool = True

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        if self.form_class.is_valid():
            self.form_class.save(commit=False)
            if self.filter_organization:
                self.form_class.instance.organization = (
                    self.request.user.profile.organization
                )
            self.form_class.save()
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
                "message": self.form_class.errors,
            },
            status=400,
        )


class MontaUpdateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.UpdateView
):
    """
    View for updating an object, with a Json response.
    """

    permission_required = None
    form_class = None

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "result": "success",
                    "message": "Record Updated Successfully!",
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


class MontaDetailView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DetailView
):
    """
    View for displaying an object, return a queryset.
    """
    model: type[Model] = None  # I WAS RIGHT
    template_name: str = None
    permission_required: str | None = None
    organization_filter: bool = True
    select_related: list[str] | None = None

    def get_queryset(self) -> QuerySet:
        """
        Method to get the queryset for the driver edit page.

        :return: The queryset for the driver edit page.
        :rtype: QuerySet | None
        """
        queryset = (
            super()
            .get_queryset()
            .filter(pk__exact=self.kwargs["pk"])
        )
        if self.organization_filter:
            queryset = queryset.filter(
                organization__exact=self.request.user.profile.organization
            )
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        return queryset


class MontaDeleteView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DeleteView
):
    """
    View for deleting an object, with a Json response.
    """

    model = None
    permission_required = None
    form_class = None

    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> JsonResponse:
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

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> None:
        """

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: None
        """
        raise exceptions.MethodNotAllowed


class MontaSearchView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    """
    View for searching an object, with a template response
    """

    permission_required: None = None
    template_name = None
    model: None = None
    form_class: None = None
    search_vector: None = None
    filter_organization: bool = True

    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handle GET requests: search the object and return a HttpResponse.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A HttpResponse
        """
        form = self.form_class(request.GET)
        query = request.GET["query"] if "query" in request.GET else None
        results = []
        if query:
            form = self.form_class({"query": query})
            search_query: SearchQuery = SearchQuery(query)
            if self.filter_organization:
                results = (
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
                results = (
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
