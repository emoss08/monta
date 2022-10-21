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
from typing import final, Any

# Core Django Imports
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

# Third Party Imports
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_user.models import Organization


@final
class GoogleRouteAvoidanceChoices(models.TextChoices):
    """Google Route Avoidance Choices"""

    TOLLS = "tolls", "Tolls"
    HIGHWAYS = "highways", "Highways"
    FERRIES = "ferries", "Ferries"


@final
class GoogleRouteModelChoices(models.TextChoices):
    """Google Route Model Choices"""

    BEST_GUESS = "best_guess", "Best Guess"
    OPTIMISTIC = "optimistic", "Optimistic"
    PESSIMISTIC = "pessimistic", "Pessimistic"


@final
class GoogleRouteDistanceUnitChoices(models.TextChoices):
    """Google Route Distance Unit Choices"""

    METRIC = "metric", "Metric"
    IMPERIAL = "imperial", "Imperial"


class Route(TimeStampedModel):
    """
    Route Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="routes",
        related_query_name="route",
        verbose_name=_("Organization"),
        help_text=_("Organization"),
    )
    origin = models.CharField(
        _("Origin"),
        max_length=255,
        help_text=_("Origin of the route"),
        blank=True,
        null=True,
    )
    destination = models.CharField(
        _("Destination"),
        max_length=255,
        help_text=_("Destination"),
        blank=True,
        null=True,
    )
    distance = models.DecimalField(
        _("Mileage"),
        help_text=_("Mileage"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    duration = models.DurationField(
        _("Duration"), help_text=_("Duration in seconds"), blank=True, null=True
    )

    class Meta:
        """
        Metaclass for Route model
        """

        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering: list[str] = ["-created"]
        indexes: list[models.Index] = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Route model

        :return: String representation of the Route model
        :rtype: str
        """
        return f"{self.origin} - {self.destination}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the Route model

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        if self.origin == self.destination:
            self.distance = 0
            self.duration = 0
        super(Route, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the Route model

        :return: Absolute url for the Route model
        :rtype: str
        """
        return reverse("route_detail", kwargs={"pk": self.pk})


# class RouteConfiguration(TimeStampedModel):
#     organization = models.OneToOneField(
#         Organization,
#         on_delete=models.CASCADE,
#         related_name="route_configuration",
#         verbose_name=_("Organization")
#     )
#     name = models.CharField(
#         _("Name"),
#         max_length=255,
#         blank=True,
#         null=True
#     )
#     route_avoidance = models.CharField(
#         _("Route Avoidance"),
#         max_length=255,
#         choices=GoogleRouteAvoidanceChoices.choices,
#         blank=True,
#         null=True
#     )
