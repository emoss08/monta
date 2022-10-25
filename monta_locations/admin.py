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
# Core Django imports
from django.contrib import admin

# Monta Imports
from monta_locations import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "location_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
        "created",
        "modified",
    )
    list_filter: tuple[str, ...] = (
        "state",
        "city",
        "zip_code",
    )
    search_fields: tuple[str, ...] = (
        "location_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )


@admin.register(models.LocationContact)
class LocationContactAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "location",
        "name",
        "created",
        "modified",
    )
    list_filter: tuple[str, ...] = (
        "location",
        "name",
    )
    search_fields: tuple[str, ...] = (
        "location",
        "name",
    )
