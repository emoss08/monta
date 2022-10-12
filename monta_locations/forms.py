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
from typing import Type

# Core Django Imports
from django import forms
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from localflavor.us.forms import USStateSelect, USZipCodeField

# Monta Imports
from monta_locations import models


class AddLocationForm(forms.ModelForm):
    """
    Form for adding a location to the database.

    name(CharField): The name of the location.
    description(CharField): The description of the location.
    address_line_1(CharField): The address line 1 of the location.
    address_line_2(CharField): The address line 2 of the location.
    city(CharField): The city of the location.
    state(USStateSelect): The state of the location.
    zip_code(USZipCodeField): The zip code of the location.

    Args:
        forms.ModelForm (ModelForm): Django ModelForm class.
    """

    name = forms.CharField(
        max_length=255,
        help_text=_("Name of the Location"),
        error_messages={
            "required": _("Please enter a name for the Location"),
            "max_length": _("Location name must be less than 255 characters"),
            "unique": _("A Location with this name already exists"),
        },
    )
    description = forms.CharField(
        help_text=_("Name of the Location"),
        required=False,
    )
    address_line_1 = forms.CharField(
        max_length=255,
        help_text=_("Address Line 1"),
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    address_line_2 = forms.CharField(
        max_length=255,
        help_text=_("Address Line 2"),
        required=False,
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    city = forms.CharField(
        max_length=255,
        help_text=_("City"),
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    state = USStateSelect()
    zip_code = USZipCodeField(
        help_text=_("Zip Code"),
    )

    class Meta:
        """
        Metaclass for AddLocationForm.
        """

        model: Type[models.Location] = models.Location
        fields = (
            "name",
            "description",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "zip_code",
        )


class UpdateLocationForm(forms.Form):
    """
    Form for adding a location to the database.

    name(CharField): The name of the location.
    description(CharField): The description of the location.
    address_line_1(CharField): The address line 1 of the location.
    address_line_2(CharField): The address line 2 of the location.
    city(CharField): The city of the location.
    state(USStateSelect): The state of the location.
    zip_code(USZipCodeField): The zip code of the location.

    Args:
        forms.ModelForm (ModelForm): Django ModelForm class.
    """

    name = forms.CharField(
        max_length=255,
        help_text=_("Name of the Location"),
        error_messages={
            "required": _("Please enter a name for the Location"),
            "max_length": _("Location name must be less than 255 characters"),
            "unique": _("A Location with this name already exists"),
        },
    )
    description = forms.CharField(
        help_text=_("Name of the Location"),
        required=False,
    )
    address_line_1 = forms.CharField(
        max_length=255,
        help_text=_("Address Line 1"),
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    address_line_2 = forms.CharField(
        max_length=255,
        help_text=_("Address Line 2"),
        required=False,
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    city = forms.CharField(
        max_length=255,
        help_text=_("City"),
        error_messages={
            "max_length": _("Location name must be less than 255 characters"),
        },
    )
    state = USStateSelect()
    zip_code = USZipCodeField(
        help_text=_("Zip Code"),
    )

    def save(self, location: models.Location):
        """
        Save the form to the database.

        Args:
            location (models.Location): The location to update.

        Returns:
            None
        """
        location.name = self.cleaned_data["name"]
        location.description = self.cleaned_data["description"]
        location.address_line_1 = self.cleaned_data["address_line_1"]
        location.address_line_2 = self.cleaned_data["address_line_2"]
        location.city = self.cleaned_data["city"]
        location.state = self.cleaned_data["state"]
        location.zip_code = self.cleaned_data["zip_code"]
        location.save()
