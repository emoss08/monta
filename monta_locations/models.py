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

# Standard Python library imports
from typing import Any

# Core Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from localflavor.us.models import USStateField, USZipCodeField
from django_extensions.db.models import TimeStampedModel

from monta_driver.models import CommentType

# Monta Imports
from monta_user.models import Organization


class Location(TimeStampedModel):
    """
    Location Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="locations",
        related_query_name="location",
        verbose_name=_("Organization"),
    )
    location_id = models.SlugField(
        _("Location ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique ID for this location."),
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name of the location."),
        unique=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Description of the location."),
        blank=True,
        null=True,
    )
    address_line_1 = models.CharField(
        _("Address Line 1"),
        max_length=255,
        help_text=_("Address Line 1"),
    )
    address_line_2 = models.CharField(
        _("Address Line 2"),
        max_length=255,
        help_text=_("Address Line 2"),
        blank=True,
        null=True,
    )
    city = models.CharField(
        _("City"),
        max_length=255,
        help_text=_("City"),
    )
    state = USStateField(
        _("State"),
        help_text=_("State"),
    )
    zip_code = USZipCodeField(
        _("Zip Code"),
        help_text=_("Zip Code"),
    )
    longitude = models.FloatField(
        _("Longitude"),
        help_text=_("Longitude"),
        blank=True,
        null=True,
    )
    latitude = models.FloatField(
        _("Latitude"),
        help_text=_("Latitude"),
        blank=True,
        null=True,
    )
    place_id = models.CharField(
        _("Place ID"),
        max_length=255,
        help_text=_("Place ID"),
        blank=True,
        null=True,
    )
    is_geocoded = models.BooleanField(
        _("Is Geocoded"),
        default=False,
        help_text=_("Is the location geocoded?"),
    )

    class Meta:
        """
        Meta Class for Location Model
        """

        verbose_name: str = _("Location")
        verbose_name_plural: str = _("Locations")
        ordering: tuple[str, ...] = ("location_id", "name")
        indexes: list[models.Index] = [
            models.Index(fields=["location_id", "name"]),
        ]

    def __str__(self) -> str:
        """
        :return: String representation of the location.
        :rtype: str
        """
        return f"{self.location_id} - {self.name}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the location.

        :param kwargs: Keyword arguments.
        :type kwargs: Any
        :return None
        :rtype None
        """
        if not self.location_id:
            self.location_id = slugify(self.name)
        super(Location, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        :return: Absolute URL for the location.
        :rtype: str
        """
        return reverse("location_detail", kwargs={"pk": self.pk})

    @property
    def get_address_combination(self) -> str:
        """
        :return: Address combination for the location.
        :rtype: str
        """
        return f"{self.address_line_1} {self.address_line_2}, {self.city} {self.state}, {self.zip_code}"


class LocationContact(TimeStampedModel):
    """
    Location Contact Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="location_contacts",
        related_query_name="location_contact",
        verbose_name=_("Organization"),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name=_("Location"),
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name of the contact."),
    )
    email = models.EmailField(
        _("Email"),
        max_length=255,
        help_text=_("Email of the contact."),
        null=True,
        blank=True,
    )
    phone = models.PositiveIntegerField(
        _("Phone"),
        help_text=_("Phone of the contact."),
        null=True,
        blank=True,
    )
    fax = models.PositiveIntegerField(
        _("Fax"),
        help_text=_("Fax of the contact."),
        null=True,
        blank=True,
    )

    class Meta:
        """
        Meta Class for LocationContact Model
        """

        verbose_name: str = _("Location Contact")
        verbose_name_plural: str = _("Location Contacts")
        ordering: tuple[str] = ("name",)
        indexes: list[models.Index] = [
            models.Index(fields=["name"]),
        ]

    def clean(self) -> None:
        """
        Clean the location contact.

        :return None
        :rtype None
        """
        if not self.email or self.phone:
            raise ValidationError(_("Must have either an email or phone number."))

    def __str__(self) -> str:
        """
        :return: String representation of the location contact.
        :rtype: str
        """
        return str(self.name)

    def get_absolute_url(self) -> str:
        """
        :return: Absolute URL for the location contact.
        :rtype: str
        """
        return reverse("location_contact_detail", kwargs={"pk": self.pk})


class LocationComment(TimeStampedModel):
    """
    Location Comment Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="location_comments",
        related_query_name="location_comment",
        verbose_name=_("Organization"),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="location_comments",
        related_query_name="location_comment",
        verbose_name=_("Location"),
    )
    comment_type = models.ForeignKey(
        CommentType,
        on_delete=models.CASCADE,
        related_name="location_comments",
        related_query_name="location_comment",
        verbose_name=_("Comment Type"),
    )
    comment = models.TextField(
        _("Comment"),
        help_text=_("Comment"),
    )

    class Meta:
        """
        Meta Class for LocationComment Model
        """

        verbose_name: str = _("Location Comment")
        verbose_name_plural: str = _("Location Comments")
        ordering: tuple[str] = ("comment_type",)
        indexes: list[models.Index] = [
            models.Index(fields=["comment"]),
        ]

    def __str__(self) -> str:
        """
        :return: String representation of the location comment.
        :rtype: str
        """
        return f"{self.comment_type} - {self.comment}"

    def get_absolute_url(self) -> str:
        """
        :return: Absolute URL for the location comment.
        :rtype: str
        """
        return reverse("location_comment_detail", kwargs={"pk": self.pk})
