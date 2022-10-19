# -*- coding: utf-8 -*-
from django.contrib import admin

from monta_routes import models


@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin[models.Route]):
    list_display = (
        "organization",
        "origin",
        "destination",
        "distance",
        "duration",
        "created",
        "modified",
    )
    list_filter = (
        "organization",
        "origin",
        "destination",
        "created",
        "modified",
    )
    search_fields = (
        "organization",
        "origin",
        "destination",
        "created",
        "modified",
    )
