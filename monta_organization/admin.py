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

# Standard library imports
from typing import Literal

# Core Django Imports
from django.contrib import admin

# Monta Imports
from monta_organization import models

admin.site.register(models.OrganizationSettings)


@admin.register(models.Integration)
class Integration(admin.ModelAdmin[models.Integration]):
    list_display: tuple[str] = ("organization", "name", "api_key")
    list_filter: tuple[str] = ("organization", "name")
    search_fields: tuple[str] = ("organization", "name", "api_key")
    ordering: tuple[str] = ("organization", "name")
    filter_horizontal: tuple[None] = ()
    list_per_page: Literal[25] = 25
