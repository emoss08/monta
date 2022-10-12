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
from typing import Literal

# Core Django Imports
from django.contrib import admin

# Monta Imports
from monta_equipment.models import Equipment, EquipmentType


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    """Equipment Type Admin"""

    list_display = ("equip_type_id", "name", "description", "created", "modified")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Equipment Admin"""

    list_display = (
        "equip_id",
        "equipment_type",
        "description",
        "vin_number",
        "primary_driver",
        "secondary_driver",
        "vehicle_model",
        "vehicle_make",
        "vehicle_year",
        "created",
        "modified",
    )
    list_filter: tuple[Literal["organization"], Literal["is_active"]] = (
        "organization",
        "is_active",
    )
    search_fields: tuple[
        Literal["equip_id"], Literal["description"], Literal["vin_number"]
    ] = ("equip_id", "description", "vin_number")
    list_select_related: Literal[True] = True
