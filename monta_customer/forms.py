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

# Standard Python Imports
from typing import Type

# Core Django Imports
from django import forms

# Monta Imports
from monta_customer import models


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
        fields: list[str] = ["name", "description"]
