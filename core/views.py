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

from typing import Any

from braces import views
from django.contrib.auth import mixins
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.views import generic


class MontaTemplateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    template_name = None
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
    mixins.LoginRequiredMixin,
    views.PermissionRequiredMixin,
    generic.CreateView
):
    """
    View for creating a new object, with a Json response.
    """
    permission_required = None
    form_class = None

    def post(
            self,
            request: ASGIRequest,
            *args: Any,
            **kwargs: Any
    ) -> JsonResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        form = self.get_form()
        if form.is_valid():
            form.save(commit=False)
            form.instance.organization = self.request.user.profile.organization
            form.save()
            return JsonResponse({
                "result": "success",
                "message": "New Record Created Successfully!",
            }, status=201)
        return JsonResponse({
            "result": "error",
            "message": form.errors,
        }, status=400)


class MontaUpdateView(
    mixins.LoginRequiredMixin,
    views.PermissionRequiredMixin,
    generic.UpdateView
):
    """
    View for updating an object, with a Json response.
    """
    permission_required = None
    form_class = None

    def post(
            self,
            request: ASGIRequest,
            *args: Any,
            **kwargs: Any
    ) -> JsonResponse:
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
            return JsonResponse({
                "result": "success",
                "message": "Record Updated Successfully!",
            }, status=201)
        return JsonResponse({
            "result": "error",
            "message": form.errors,
        }, status=400)


class MontaDeleteView(mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DeleteView):
    """
    View for deleting an object, with a Json response.
    """
    model = None
    permission_required = None

    def get(
            self,
            request: ASGIRequest,
            *args: Any,
            **kwargs: Any
    ) -> JsonResponse:
        """
        Handle DELETE requests: delete the object and return a JsonResponse.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: A JsonResponse
        """
        self.get_object().delete()
        return JsonResponse({
            "result": "success",
            "message": "Record Deleted Successfully!",
        }, status=204)
