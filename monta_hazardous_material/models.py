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
from django.db import models
from django.urls import reverse

# Third Party Imports
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_user.models import Organization


class HazardousClass(TimeStampedModel):
    """
    Hazardous Class Model Fields

    organization: Organization Model Foreign Key
    name: Name of the Hazardous Class
    description: Description of the Hazardous Class

    ----------------------------------------
    Reference:(https://www.fmcsa.dot.gov/regulations/enforcement/nine-classes-hazardous-materials-yellow-visor-card)
    ----------------------------------------
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="hazardous_classes",
        related_query_name="hazardous_class",
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        """
        Meta Class for HazardousClass Model

        verbose_name: Hazardous Class
        verbose_name_plural: Hazardous Classes
        ordering: the ordering of the HazardousClass Model
        indexes: indexes for the HazardousClass Model
        """

        verbose_name = "Hazardous Class"
        verbose_name_plural = "Hazardous Classes"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of HazardousClass Model

        Returns:
            str: String representation of HazardousClass Model
        """
        return self.name

    def save(self, **kwargs):
        """
        Save HazardousClass Model

        Args:
            **kwargs: Keyword Arguments
        """
        self.name = self.name.upper()
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get Absolute URL of HazardousClass Model

        Returns:
            str: Absolute URL of HazardousClass Model
        """
        return reverse(
            "monta_hazardous_material:hazardousclass_detail", kwargs={"pk": self.pk}
        )
