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
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

# Monta Imports
from monta_user.models import Organization, MontaUser


class Fleet(TimeStampedModel):
    """
    Fleet Model Fields

    fleet_id: The fleet id.
    name: The name of the fleet.
    fleet_manager: The fleet manager of the fleet.
    description: The description of the fleet.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="fleets",
        related_query_name="fleet",
        verbose_name=_("Organization"),
        help_text=_("Organization that the fleet belongs to."),
    )
    name = models.CharField(
        _("Name"),
        max_length=50,
        unique=True,
        help_text=_("Name of the fleet."),
    )
    fleet_id = models.CharField(
        _("Fleet ID"),
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Unique ID of the fleet."),
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
        help_text=_("Description of the fleet."),
    )
    fleet_manager = models.ForeignKey(
        MontaUser,
        on_delete=models.PROTECT,
        related_name="fleets",
        related_query_name="fleet",
        verbose_name=_("Fleet Manager"),
        help_text=_("The user who manages this fleet"),
        null=True,
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Is the fleet active?"),
    )

    class Meta:
        """
        Meta class for Fleet.

        Attributes:
            verbose_name (str): Verbose name for Fleet.
            verbose_name_plural (str): Verbose name for Fleet.
            ordering (list): Ordering for Fleet.
            indexes (list): Indexes for Fleet.
        """

        ordering = ["name"]
        verbose_name = _("Fleet")
        verbose_name_plural = _("Fleets")
        indexes = [
            models.Index(fields=["name", "fleet_id"]),
        ]

    def __str__(self) -> str:
        """
        Return the string representation of the fleet.

        Returns:
            str: String representation of the fleet.
        """
        return f"Fleet {self.fleet_id}, {self.name} for managed by {self.fleet_manager}"

    def save(self, **kwargs) -> None:
        """
        Save the fleet.

        Args:
            **kwargs: Keyword arguments.

        Returns:
            None
        """
        self.full_clean()
        if not self.fleet_id:
            self.fleet_id = self.name[:9].replace(" ", "").upper() + str(
                int(Fleet.objects.count() + 1)
            )
        self.fleet_id = self.fleet_id.upper()
        super(Fleet, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Return the absolute url for the fleet.

        Returns:
            str: Absolute url for the fleet.
        """
        return reverse("fleet", kwargs={"pk": self.pk})
