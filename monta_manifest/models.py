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
from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _

# Core Django Imports
from django_extensions.db.models import TimeStampedModel

from monta_order.models import Order, StatusChoices

# Monta Imports
from monta_user.models import Organization


@final
class Manifest(TimeStampedModel):
    """
    Manifest Model
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="manifests",
        related_query_name="manifest",
        verbose_name=_("Organization"),
    )
    manifest_number = models.CharField(
        _("Manifest Number"),
        max_length=255,
        unique=True,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
        verbose_name=_("Status"),
    )
    orders = models.ManyToManyField(
        Order,
        related_name="manifests",
        related_query_name="manifest",
        verbose_name=_("Orders"),
        help_text=_("Orders to be included in the manifest."),
    )

    class Meta:
        verbose_name: str = _("Manifest")
        verbose_name_plural: str = _("Manifests")
        ordering: list[str] = ["-created"]

    def __str__(self) -> str:
        return self.manifest_number

    def generate_manifest_number(self) -> str:
        """
        Generate a manifest number

        :return: new_manifest_number
        :rtype: str
        """
        last_manifest = self.objects.filter(
            organization=self.organization,
        ).last()
        if last_manifest:
            last_manifest_number = last_manifest.manifest_number
            last_manifest_number = int(last_manifest_number[1:])
            new_manifest_number: str = "M" + str(last_manifest_number + 1)
        else:
            new_manifest_number = "M1"
        return new_manifest_number

    def clean(self) -> None:
        pass

    def save(self, **kwargs) -> None:
        pass

    def get_absolute_url(self) -> str:
        pass
