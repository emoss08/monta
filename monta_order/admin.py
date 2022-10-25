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

from monta_order import models


@admin.register(models.Movement)
class MovementAdmin(admin.ModelAdmin):
    """Movement Admin"""

    list_display: tuple[str, ...] = (
        "id",
        "status",
        "order",
        "created",
        "modified",
    )


@admin.register(models.ServiceIncident)
class ServiceIncidentAdmin(admin.ModelAdmin):
    """ServiceIncident Admin"""

    list_display: tuple[str, ...] = (
        "id",
        "stop",
        "created",
        "modified",
    )


class OrderDocumentationAdmin(admin.TabularInline):
    """OrderDocumentation Admin"""

    model: Type[models.OrderDocumentation] = models.OrderDocumentation
    verbose_name_plural: str = "Order Documentation"
    extra: int = 0


@admin.register(models.Stop)
class StopAdmin(admin.ModelAdmin):
    """Stop Admin"""

    list_display: tuple[str, ...] = (
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

    list_display: tuple[str, ...] = (
        "name",
        "description",
        "created",
        "modified",
    )


@admin.register(models.DelayCode)
class DelayCodeAdmin(admin.ModelAdmin):
    """Delay Code Admin"""

    list_display: tuple[str, ...] = (
        "name",
        "description",
        "created",
        "modified",
    )


@admin.register(models.Commodity)
class CommodityAdmin(admin.ModelAdmin):
    """Commodity Admin"""

    list_display: tuple[str, ...] = (
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

    list_display: tuple[str, ...] = (
        "code",
        "description",
    )
    search_fields: tuple[str, ...] = (
        "code",
        "description",
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin"""

    list_display: tuple[str, ...] = (
        "order_id",
        "status",
        "order_type",
        "commodity",
        "created",
        "modified",
    )

    inlines: tuple[Type[OrderDocumentationAdmin]] = (OrderDocumentationAdmin,)
