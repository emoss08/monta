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

from django.contrib import admin

from monta_locations import models


class LocationContactAdmin(admin.TabularInline):
    model: Type[models.LocationContact] = models.LocationContact
    verbose_name_plural: str = "Location Contact"
    extra: int = 0


@admin.register(models.Location)
class LocationInline(admin.ModelAdmin):
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
    inlines: tuple[
        Type[LocationContactAdmin],
    ] = (
        LocationContactAdmin,
    )
