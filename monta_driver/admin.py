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
from monta_driver.models import (
    CommentType,
    DriverProfile,
    DriverContact,
    DriverQualification,
    DriverComment,
    Driver,
)


# Register your models here.
@admin.register(CommentType)
class CommentTypeInline(admin.ModelAdmin):
    """Comment Type Admin"""

    list_display = ("name", "description", "created", "modified")


class DriverProfileInline(admin.StackedInline):
    """Driver Profile Inline"""

    model: Type[DriverProfile] = DriverProfile
    can_delete = False
    verbose_name_plural = "Driver Profile"


class DriverContactInline(admin.StackedInline):
    """Driver Contact Inline"""

    model: Type[DriverContact] = DriverContact
    can_delete = False
    verbose_name_plural = "Driver Contact"
    list_select_related = True


class DriverQualificationInline(admin.StackedInline):
    """Driver Qualification Inline"""

    model: Type[DriverQualification] = DriverQualification
    can_delete = False
    verbose_name_plural = "Driver Qualifications"


class DriverCommentInline(admin.StackedInline):
    """Driver Comment Inline"""

    model: Type[DriverComment] = DriverComment
    can_delete = False
    verbose_name_plural = "Driver Comments"


@admin.register(Driver)
class DriverInline(admin.ModelAdmin):
    """Driver Admin"""

    list_display = ("driver_id", "first_name", "last_name")
    inlines = (
        DriverProfileInline,
        DriverContactInline,
        DriverQualificationInline,
        DriverCommentInline,
    )


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    """Driver Profile Admin"""

    list_display = (
        "driver",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )
    list_select_related = True


@admin.register(DriverContact)
class DriverContactAdmin(admin.ModelAdmin):
    """Driver Contact Admin"""

    list_display = ("driver", "contact_name", "contact_phone")
    list_select_related = True
