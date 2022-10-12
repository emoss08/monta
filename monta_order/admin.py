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
from django.contrib import admin

# Monta Imports
from monta_order import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin"""

    list_display = (
        "order_id",
        "status",
        "order_type",
        "commodity",
        "created",
        "modified",
    )


@admin.register(models.Movement)
class MovementAdmin(admin.ModelAdmin):
    """Movement Admin"""

    list_display = (
        "id",
        "status",
        "order",
        "created",
        "modified",
    )


@admin.register(models.ServiceIncident)
class ServiceIncidentAdmin(admin.ModelAdmin):
    """ServiceIncident Admin"""

    list_display = (
        "id",
        "stop",
        "created",
        "modified",
    )


@admin.register(models.OrderDocumentation)
class OrderDocumentationAdmin(admin.ModelAdmin):
    """OrderDocumentation Admin"""

    list_display = (
        "id",
        "order",
        "created",
        "modified",
    )


@admin.register(models.Stop)
class StopAdmin(admin.ModelAdmin):
    """Stop Admin"""

    list_display = (
        "id",
        "sequence",
        "status",
        "movement",
        "created",
        "modified",
    )


@admin.register(models.OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    """Order Type Admin"""

    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )


@admin.register(models.DelayCode)
class DelayCodeAdmin(admin.ModelAdmin):
    """Delay Code Admin"""

    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )


@admin.register(models.Commodity)
class CommodityAdmin(admin.ModelAdmin):
    """Commodity Admin"""

    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )


@admin.register(models.RevenueCode)
class RevenueCodeAdmin(admin.ModelAdmin):
    """
    Revenue Code Admin
    """

    list_display = (
        "code",
        "description",
    )
    search_fields = (
        "code",
        "description",
    )
