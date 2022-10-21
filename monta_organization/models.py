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
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_user.models import Organization
from monta_routes.models import GoogleRouteDistanceUnitChoices, GoogleRouteModelChoices


@final
class IntegrationChoices(models.TextChoices):
    """
    Google API Choices
    """

    GOOGLE_MAPS = "google_maps", _("Google Maps")
    GOOGLE_PLACES = "google_places", _("Google Places")


class OrganizationSettings(TimeStampedModel):
    """
    Organization Settings Model
    """

    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name=_("Organization"),
        help_text=_("The organization that the settings belong to."),
    )
    timezone = models.CharField(
        _("Timezone"),
        max_length=255,
        default="America/New_York",
        help_text=_("The timezone of the organization"),
    )
    language = models.CharField(
        _("Language"),
        max_length=255,
        default="en",
        help_text=_("The language of the organization"),
    )
    currency = models.CharField(
        _("Currency"),
        max_length=255,
        default="USD",
        help_text=_("The currency that the organization uses"),
    )
    date_format = models.CharField(
        _("Date Format"),
        max_length=255,
        default="MM/DD/YYYY",
        help_text=_("Date Format"),
    )
    time_format = models.CharField(
        _("Time Format"), max_length=255, default="HH:mm", help_text=_("Time Format")
    )
    mileage_unit = models.CharField(
        _("Mileage Unit"),
        max_length=255,
        choices=GoogleRouteDistanceUnitChoices.choices,
        default=GoogleRouteDistanceUnitChoices.IMPERIAL,
        help_text=_("The mileage unit that the organization uses"),
    )
    traffic_model = models.CharField(
        _("Traffic Model"),
        max_length=255,
        choices=GoogleRouteModelChoices.choices,
        default=GoogleRouteModelChoices.BEST_GUESS,
        help_text=_("The traffic model that the organization uses"),
    )
    generate_routes = models.BooleanField(
        _("Generate Routes"),
        default=False,
        help_text=_("Generate routes for the organization"),
    )

    class Meta:
        """
        Metaclass for OrganizationSettings
        """

        verbose_name: str = _("Organization Settings")
        verbose_name_plural: str = _("Organization Settings")

    def __str__(self) -> str:
        """
        Return the string representation of the settings

        :return: The string representation of the settings
        :rtype: str
        """
        return f"{self.organization.name} Settings"

    def save(self, **kwargs: Any) -> None:
        """
        Save the settings

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        return super(OrganizationSettings, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the OrganizationSettings

        :return: The absolute url for the OrganizationSettings
        :rtype: str
        """
        return reverse("organization_settings", kwargs={"pk": self.pk})


class Integration(TimeStampedModel):
    """
    Integration Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="integrations",
    )
    is_active = models.BooleanField(
        _("Is Active"), default=False, help_text=_("Is the integration active?")
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        choices=IntegrationChoices.choices,
    )
    api_key = models.CharField(
        _("API Key"),
        max_length=255,
        help_text=_("API Key"),
        null=True,
        blank=True,
    )
    client_id = models.CharField(
        _("Client ID"),
        max_length=255,
        null=True,
        blank=True,
    )
    client_secret = models.CharField(
        _("Client Secret"),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """
        Metaclass for Integration
        """

        verbose_name: str = _("Integration")
        verbose_name_plural: str = _("Integrations")
        ordering: list[str] = ["name"]
        indexes: list[models.Index] = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Integration

        :return: The string representation of the Integration
        :rtype: str
        """
        return f"{self.name}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the Integration

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the Integration

        :return: The absolute url of the Integration
        :rtype: str
        """
        return reverse("integration_detail", kwargs={"pk": self.pk})
