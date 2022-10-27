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

from typing import Type, TypeVar

from braces import views
from django.contrib.auth import mixins
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import Model, ModelBase
from django.forms.models import ModelForm, ModelFormMetaclass
from django.views import generic

_T = TypeVar("_T", bound=str)


class MontaGenericTemplateView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    template_name: _T

    def _check_template_attr(self):
        if not isinstance(self.template_name, str):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the template_name to be an string. "
                "Check your template_name attribute."
            )


class MontaGenericCreateView(
    mixins.LoginRequiredMixin, generic.CreateView, views.PermissionRequiredMixin
):
    """
    MontaGenericCreateView is a generic view that is used to create a model instance.
    """

    model: Model
    template_name: str
    form_class: Type[ModelForm]
    permission_required: str

    def _check_model_attr(self) -> None:
        if not isinstance(self.model, ModelBase):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the model to be an instance of django.db.models.base.Model. "
                "Check your model attribute."
            )

    def _check_form_attr(self) -> None:
        if not isinstance(self.form_class, ModelFormMetaclass):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the form_class to be an instance of ModelForm. "
                "Check your form_class attribute. You may have forms.Form instead of "
                "forms.ModelForm."
            )

    def _check_template_attr(self) -> None:
        if self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the template_name to be None. "
                "Check your template_name attribute."
            )


class MontaGenericUpdateView(MontaGenericCreateView):
    """
    A generic view for updating a model instance.
    """


class MontaGenericDetailView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DetailView
):
    """
    A generic view for getting details of a model instance.
    """

    model: Type[Model]
    template_name: str
    permission_required: str

    def _check_model_attr(self) -> None:
        if not isinstance(self.model, ModelBase):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the model to be an instance of django.db.models.base.Model. "
                "Check your model attribute."
            )

    def _check_template_attr(self) -> None:
        if self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the template_name to be None. "
                "Check your template_name attribute."
            )


class MontaGenericDeleteView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.DeleteView
):
    """
    MontaGenericDeleteView is a generic view that is used to create a model instance.
    """

    model: Type[Model]
    template_name: str
    permission_required: str
    form_class: None

    def _check_model_attr(self) -> None:
        if not isinstance(self.model, ModelBase):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the model to be an instance of django.db.models.base.Model. "
                "Check your model attribute."
            )

    def _check_form_attr(self) -> None:
        if self.form_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the form_class to be None. "
                "Check your form_class attribute."
            )

    def _check_template_attr(self) -> None:
        if self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires the template_name to be None. "
                "Check your template_name attribute."
            )
