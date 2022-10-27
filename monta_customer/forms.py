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

from typing import Type

from django import forms

from monta_customer import models


class AddCustomerForm(forms.ModelForm):
    """
    AddCustomerForm Class
    """

    class Meta:
        model: Type[models.Customer] = models.Customer
        fields: tuple[str, ...] = (
            "organization",
            "is_active",
            "customer_id",
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "zip_code"
        )


class AddDocumentClassificationsForm(forms.ModelForm):
    """
    AddDocumentClassificationsForm class
    """

    name = forms.CharField(
        max_length=255, help_text="Name of the document classification"
    )
    description = forms.CharField(
        max_length=255,
        help_text="Description of the document classification",
        required=False,
    )

    class Meta:
        """
        Metaclass for AddDocumentClassificationsForm
        """

        model: Type[models.DocumentClassification] = models.DocumentClassification
        fields: tuple[str, ...] = ("name", "description")
