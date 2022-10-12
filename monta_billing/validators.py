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
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value) -> None:
    """
    Validate file extension
    """
    if not value.name.endswith(".csv"):
        raise ValidationError(
            _("%(value)s is not a valid file extension"),
            params={"value": value},
        )


def validate_file_size(value) -> None:
    """
    Validate file size
    """
    limit: int = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            _("%(value)s file too large. Size should not exceed 2 MiB."),
            params={"value": value},
        )
