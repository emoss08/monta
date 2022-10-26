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

from braces import views
from django.contrib.auth import mixins
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.asgi import ASGIRequest
from django.db.models.base import Model, ModelBase
from django.forms.models import ModelForm, ModelFormMetaclass
from django.views import generic

from core import exceptions


class MontaGenericCreateView(
    mixins.LoginRequiredMixin, generic.CreateView, views.PermissionRequiredMixin
):
    template_name: str
    form_class: Type[ModelForm]
    permission_required: str

    def __init__(self) -> None:
        """
        Initialize the view.
        """
        super().__init__()
        if not isinstance(self.form_class, ModelFormMetaclass):
            raise ImproperlyConfigured(
                "{0} requires the form_class to be an instance of ModelForm. "
                "Check your form_class attribute. You may have forms.Form instead of "
                "forms.ModelForm.".format(self.__class__.__name__)
            )
        if not isinstance(self.permission_required, str):
            raise ImproperlyConfigured(
                "{0} requires the permission_required to be a string. "
                "Check your permission_required attribute.".format(self.__class__.__name__)
            )
        # Disable the ability to use the template_name attribute. This is because you can
        # utilize generic.CreateView alone for the template_name attribute.
        if self.template_name:
            raise ImproperlyConfigured(
                "{0} requires the template_name to be None. "
                "Check your template_name attribute.".format(self.__class__.__name__)
            )


class MontaGenericUpdateView(MontaGenericCreateView):
    pass


class MontaGenericDetailView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DetailView
):
    model: Type[Model]
    template_name: str
    permission_required: str

    def __init__(self) -> None:
        super().__init__()
        if self.template_name:
            if not isinstance(self.model, Model):
                raise ImproperlyConfigured(
                    "{0} requires the model to be an instance of Model. "
                    "Check your model attribute.".format(self.__class__.__name__)
                )
        if self.permission_required:
            if not isinstance(self.permission_required, str):
                raise ImproperlyConfigured(
                    "{0} requires the permission_required to be a string. "
                    "Check your permission_required attribute.".format(self.__class__.__name__)
                )


class MontaGenericDeleteView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DeleteView
):
    model: Type[Model]
    template_name: str
    permission_required: str
    form_class: None

    def __init__(self) -> None:
        super().__init__()
        if self.model:
            if not isinstance(self.model, ModelBase):
                raise ImproperlyConfigured(
                    "{0} requires the model to be an instance of Model. "
                    "Check your model attribute.".format(self.__class__.__name__)
                )
        if self.permission_required:
            if not isinstance(self.permission_required, str):
                raise ImproperlyConfigured(
                    "{0} requires the permission_required to be a string. "
                    "Check your permission_required attribute.".format(self.__class__.__name__)
                )
        if self.form_class:
            raise ImproperlyConfigured(
                "{0} requires the form_class to be None. "
                "Check your form_class attribute.".format(self.__class__.__name__)
            )

    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> None:
        """
        Handle POST requests: delete the object and return a JsonResponse.

        :param request: The request object
        :param args: The args
        :param kwargs: The kwargs
        :return: None
        """
        raise exceptions.MethodNotAllowed
