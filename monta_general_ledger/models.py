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

# Standard library imports
from typing import final

# Core Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_user.models import Organization


@final
class GeneralLeader(TimeStampedModel):
    """
    General Ledger Model
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="general_ledgers",
        related_query_name="general_ledger",
        verbose_name=_("Organization"),
    )
