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

# Core Django Imports
from django import forms
from django.utils.translation import gettext_lazy as _

# Monta Imports
from monta_billing import models


class AddChargeTypeForm(forms.ModelForm):
    """
    Form for adding a new charge type.
    """
    name = forms.CharField(
        max_length=100,
        help_text=_("Name of the Charge Type"),
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
    )
    description = forms.CharField(
        max_length=255,
        help_text=_("Description of the Charge Type"),
        required=False,
        error_messages={
            "max_length": _(
                "Charge Type description must be less than 255 characters."
            ),
        },
    )

    class Meta:
        """
        Meta class for AddChargeTypeForm.
        """
        model = models.ChargeType
        fields = ("name", "description")


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
        Meta class for AdditionalChargeForm.
        """
        model = models.ChargeType
        fields = (
            "order",
            "name",
            "description",
            "charge_type",
            "unit",
            "amount",
            "total_amount",
        )
