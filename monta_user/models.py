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

import uuid
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from localflavor.us.models import USStateField, USZipCodeField

from monta_user.managers import MontaUserManager

"""
Maya (https://www.twitch.tv/purplelf) made me add verbose names to all of the model fields for translation :(
Go Follow her on Twitch!
"""


class MontaUser(AbstractBaseUser, PermissionsMixin):
    """
    User Model Fields
    """

    username = models.CharField(
        _("Username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        help_text=_("Required. A valid email address."),
    )
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = MontaUserManager()

    class Meta:
        """
        Metaclass for the MontaUser model
        """

        verbose_name: str = _("User")
        verbose_name_plural: str = _("Users")
        ordering: list[str] = ["-date_joined"]

    def __str__(self) -> str:
        """
        String representation of the user

        :return: The username of the user
        :rtype: str
        """
        return str(self.username)

    def get_absolute_url(self) -> str:
        """
        Returns the url to access a particular user instance.

        :return: The url to access a particular user instance
        :rtype: str
        """
        return reverse("monta_user:user_profile_overview", kwargs={"pk": self.pk})


class Profile(TimeStampedModel):
    """
    Profile Model Fields
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="profile",
        related_query_name="profile",
        verbose_name=_("User"),
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT,
        related_name="profiles",
        related_query_name="profile",
        verbose_name=_("Organization"),
    )
    title = models.ForeignKey(
        "JobTitle",
        on_delete=models.PROTECT,
        related_name="profiles",
        related_query_name="profile",
        verbose_name=_("Title"),
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=255,
        help_text=_("The first name of the user"),
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=255,
        help_text=_("The last name of the user"),
    )
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to="profiles/",
        null=True,
        blank=True,
        help_text=_("The profile picture of the user"),
    )
    bio = models.TextField(
        _("Bio"),
        null=True,
        blank=True,
        help_text=_("The bio of the user"),
    )
    address_line_1 = models.CharField(
        _("Address"),
        max_length=100,
        help_text=_("The address of the user"),
    )
    address_line_2 = models.CharField(
        _("Address Line 2"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("The address of the user"),
    )
    city = models.CharField(
        _("City"),
        max_length=100,
        help_text=_("The city of the user"),
    )
    state = USStateField(
        _("State"),
        help_text=_("Enter the state of the user"),
    )
    zip_code = USZipCodeField(
        _("Zip Code"),
        help_text=_("Enter the zip code of the user"),
    )
    phone = models.CharField(
        _("Phone Number"),
        max_length=50,
        null=True,
        blank=True,
        help_text=_("The phone number of the user"),
    )
    email_verified = models.BooleanField(
        _("Email Verified"),
        default=False,
        help_text=_("If the user has verified their email"),
    )

    class Meta:
        """
        Metaclass for the Profile model
        """

        ordering: list[str] = ["-created"]
        verbose_name: str = _("Profile")
        verbose_name_plural: str = _("Profiles")
        indexes: list[models.Index] = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the profile

        :return: The username of the user
        :rtype: str
        """
        return str(self.user.username)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the profile

        :return: The absolute url of the profile
        :rtype: str
        """
        return reverse("monta_user:user_profile_overview", kwargs={"pk": self.pk})

    def get_user_profile_pic(self) -> str:
        """
        Get the profile picture of the user

        :return: The profile picture of the user
        :rtype: str
        """
        if self.profile_picture:
            return str(self.profile_picture)
        return "/static/media/avatars/blank.avif"

    def get_user_org_name(self) -> str:
        """
        Get the organization name of the user

        :return: The organization name of the user
        :rtype: str
        """
        if self.organization:
            return self.organization.name
        return ""

    def get_user_phone(self) -> str:
        """
        Get the phone number of the user

        :return: The phone number of the user
        :rtype: str
        """
        if self.phone:
            return self.phone
        return ""

    def get_user_zip_code(self) -> USZipCodeField | str:
        """
        Get the zip code of the user

        :return: The zip code of the user
        :rtype: str
        """
        if self.zip_code:
            return self.zip_code
        return ""

    def get_user_city(self) -> str:
        """
        Get the city of the user

        :return: The city of the user
        :rtype: str
        """
        if self.city:
            return self.city
        return ""

    def get_user_state(self) -> USStateField | str:
        """
        Get the state of the user

        :return: The state of the user
        :rtype: str
        """
        if self.state:
            return self.state
        return ""

    def get_user_address(self) -> str:
        """
        Get the address of the user

        :return: The address of the user
        :rtype: str
        """
        if self.address_line_1:
            return self.address_line_1
        return ""

    def get_user_city_state(self) -> str:
        """
        Get the city and state of the user

        :return: The city and state of the user
        :rtype: str
        """
        if self.city and self.state:
            return f"{self.city}, {self.state}"
        return ""

    def get_user_email_verification(self) -> bool:
        """
        Get the email verification status of the user

        :return: The email verification status of the user
        :rtype: bool
        """
        return self.email_verified

    def get_full_name(self) -> str:
        """
        Get the full name of the user

        :return: The full name of the user
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"


class JobTitle(TimeStampedModel):
    """
    Job Title Model Fields

    title_id: The id of the job title
    name: The name of the job title
    description: The description of the job title
    """

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="job_titles",
    )
    title_id = models.SlugField(
        _("Title ID"), max_length=255, unique=True, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        """
        Metaclass for the JobTitle model

        verbose_name: The verbose name of the model
        verbose_name_plural: The plural verbose name of the model
        ordering: The default ordering of the model
        indexes: The indexes of the model
        """

        ordering: list[str] = ["name"]
        verbose_name: str = _("Job Title")
        verbose_name_plural: str = _("Job Titles")
        indexes: list[models.Index] = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the job title

        :return: The name of the job title
        :rtype: str
        """
        return str(self.name)

    def save(self, **kwargs: Any) -> None:
        """
        Save the job title instance to the database

        :param args: The arguments
        :type args: any
        :param kwargs: The keyword arguments
        :type kwargs: any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.title_id:
            self.title_id = slugify(self.name)
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the job title

        :return: The absolute url of the job title
        :rtype: str
        """
        return reverse("job-title", kwargs={"pk": self.pk})


class Organization(TimeStampedModel):
    """
    Organization Model Fields

    org_id: The id of the organization
    name: The name of the organization
    description: The description of the organization
    profile_picture: The profile picture of the organization
    """

    name = models.CharField(_("Organization Name"), max_length=255, unique=True)
    org_id = models.UUIDField(
        _("Organization ID"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Organization Description"),
        null=True,
        blank=True,
        help_text=_("The description of the organization"),
    )
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to="organizations/", null=True, blank=True
    )

    class Meta:
        """
        Metaclass for the Organization model

        verbose_name: The verbose name of the model
        verbose_name_plural: The plural verbose name of the model
        ordering: The default ordering of the model
        indexes: The indexes of the model
        """

        ordering: list[str] = ["name"]
        verbose_name: str = _("Organization")
        verbose_name_plural: str = _("Organizations")
        indexes: list[models.Index] = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the organization

        :return: The name of the organization
        :rtype: str
        """
        return str(self.name)

    def save(self, **kwargs: Any) -> None:
        """
        Save the organization

        :param kwargs: The keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.org_id:
            self.org_id = uuid.uuid4()
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the organization

        :return: The absolute url of the organization
        :rtype: str
        """
        return reverse("", kwargs={"pk": self.pk})
