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

from monta_driver import models


@admin.register(models.CommentType)
class CommentTypeInline(admin.ModelAdmin):
    """Comment Type Admin"""

    list_display: tuple[str, ...] = ("name", "description", "created", "modified")


class DriverProfileInline(admin.StackedInline):
    """Driver Profile Inline"""

    model: Type[models.DriverProfile] = models.DriverProfile
    can_delete: bool = False
    verbose_name_plural: str = "Driver Profile"


class DriverContactInline(admin.TabularInline):
    """Driver Contact Inline"""

    model: Type[models.DriverContact] = models.DriverContact
    verbose_name_plural: str = "Driver Contact"
    list_select_related: bool = True
    extra: int = 0


class DriverQualificationInline(admin.TabularInline):
    """Driver Qualification Inline"""

    model: Type[models.DriverQualification] = models.DriverQualification
    verbose_name_plural: str = "Driver Qualifications"
    extra: int = 0


class DriverCommentInline(admin.TabularInline):
    """Driver Comment Inline"""

    model: Type[models.DriverComment] = models.DriverComment
    verbose_name_plural: str = "Driver Comments"
    extra: int = 0


@admin.register(models.Driver)
class DriverInline(admin.ModelAdmin):
    """Driver Admin"""

    list_display: tuple[str, ...] = ("driver_id", "first_name", "last_name")
    inlines: tuple[
        Type[DriverProfileInline],
        Type[DriverContactInline],
        Type[DriverQualificationInline],
        Type[DriverCommentInline],
    ] = (
        DriverProfileInline,
        DriverContactInline,
        DriverQualificationInline,
        DriverCommentInline,
    )
