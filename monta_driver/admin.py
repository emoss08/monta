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
# Standard Python Libraries
from typing import Type

# Core Django imports
from django.contrib import admin

# Monta Imports
from monta_driver import models


# Register your models here.
@admin.register(models.CommentType)
class CommentTypeInline(admin.ModelAdmin[models.CommentType]):
    """Comment Type Admin"""

    list_display = ("name", "description", "created", "modified")


class DriverProfileInline(admin.StackedInline[models.DriverProfile]):
    """Driver Profile Inline"""

    model: Type[models.DriverProfile] = models.DriverProfile
    can_delete = False
    verbose_name_plural = "Driver Profile"


class DriverContactInline(admin.TabularInline[models.DriverContact]):
    """Driver Contact Inline"""

    model: Type[models.DriverContact] = models.DriverContact
    verbose_name_plural = "Driver Contact"
    list_select_related = True
    extra: int = 0


class DriverQualificationInline(admin.TabularInline[models.DriverQualification]):
    """Driver Qualification Inline"""

    model: Type[models.DriverQualification] = models.DriverQualification
    verbose_name_plural = "Driver Qualifications"
    extra: int = 0


class DriverCommentInline(admin.TabularInline[models.DriverComment]):
    """Driver Comment Inline"""

    model: Type[models.DriverComment] = models.DriverComment
    verbose_name_plural = "Driver Comments"
    extra: int = 0


@admin.register(models.Driver)
class DriverInline(admin.ModelAdmin):
    """Driver Admin"""

    list_display = ("driver_id", "first_name", "last_name")
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
