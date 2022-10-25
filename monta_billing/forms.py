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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from django import forms
from django.utils.translation import gettext_lazy as _

from monta_billing import models


class AddChargeTypeForm(forms.ModelForm):
    """
    Form for adding a new charge type.
    """

    name = forms.CharField(
        max_length=100,
        error_messages={
            "required": _("Please enter a name for the Charge Type"),
            "max_length": _("Charge Type name must be less than 100 characters"),
            "unique": _("A Charge Type with this name already exists"),
            "NON_FIELD_ERRORS": {
                "unique": _("A Charge Type with this name already exists"),
                "unique_together": _("A Charge Type with this name already exists"),
                "duplicate_key": _("A Charge Type with this name already exists"),
            },
        },
        widget=forms.TextInput(attrs={"placeholder": "Enter Name"}),
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        error_messages={
            "max_length": _(
                "Charge Type description must be less than 255 characters."
            ),
        },
        widget=forms.Textarea(attrs={"placeholder": "Enter Description", "rows": 2}),
    )

    class Meta:
        """
        Metaclass for AddChargeTypeForm.
        """

        model: Type[models.ChargeType] = models.ChargeType
        fields: tuple[str, ...] = ("name", "description")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field("name", css_class="form-control", id="charge_type_name"),
                    css_class="col-md-6",
                ),
                Div(
                    Field("description", css_class="form-control"),
                    css_class="col-md-6",
                ),
                css_class="row",
            )
        )

        # Set the form's error messages
        self.error_messages = {
            "NON_FIELD_ERRORS": {
                "unique": _("A Charge Type with this name already exists"),
                "unique_together": _("A Charge Type with this name already exists"),
                "duplicate_key": _("A Charge Type with this name already exists"),
            },
        }

    def clean(self) -> None:
        """
        Clean the form.
        """
        super().clean()

        # Check if the charge type already exists
        if models.ChargeType.objects.filter(name=self.cleaned_data["name"]).exists():
            self.add_error(
                "name",
                forms.ValidationError(
                    self.error_messages["NON_FIELD_ERRORS"]["unique"],
                    code="unique",
                ),
            )

    def save(self, commit: bool = True) -> models.ChargeType:
        """
        Save the form.
        """
        charge_type = super().save(commit=False)
        charge_type.name = self.cleaned_data["name"]
        charge_type.description = self.cleaned_data["description"]
        if commit:
            charge_type.save()
        return charge_type


class AdditionalChargeForm(forms.ModelForm):
    """
    Form for adding a new additional charge.
    """

    order = forms.ModelChoiceField(
        queryset=models.Order.objects.all(),
    )
    name = forms.CharField(max_length=100, help_text=_("Name of the Charge Type"))
    description = forms.CharField(
        max_length=255, help_text=_("Description of the Charge Type")
    )
    charge_type = forms.ModelChoiceField(
        queryset=models.ChargeType.objects.all(),
    )
    unit = forms.IntegerField(help_text=_("Number of units for the charge"))
    amount = forms.DecimalField(help_text=_("Amount of the charge"))
    total_amount = forms.DecimalField(
        help_text=_("Total amount of the units multiplied by charge amount")
    )

    class Meta:
        """
        Metaclass for AdditionalChargeForm.
        """

        model: Type[models.ChargeType] = models.ChargeType
        fields: tuple[str, ...] = (
            "order",
            "name",
            "description",
            "charge_type",
            "unit",
            "amount",
            "total_amount",
        )
