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

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value: str) -> None:
    """
    Validate file extension
    """
    valid_extensions: list[str, ...] = [".csv", ".xls", ".xlsx"]
    if not value.endswith(tuple(valid_extensions)):
        raise ValidationError(
            _("%(value)s is not a valid file type. Valid file types are: .csv, .xls, .xlsx"),
            params={"value": value},
        )


def validate_file_size(value) -> None:
    """
    Validate file size
    """
    max_size: int = 10485760
    if value.size > max_size:
        raise ValidationError(
            _("%(value)s is too large. Maximum file size is 10MB"),
            params={"value": value},
        )
