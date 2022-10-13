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

from __future__ import annotations

# Core Django Imports
from django.db import models
from django.urls import reverse
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import functions

# Third Party Imports
from django_extensions.db.models import TimeStampedModel
from localflavor.us.models import USStateField, USZipCodeField

# Monta Imports
from monta_user.models import Organization
from monta_customer.models import DocumentClassification
from monta_fleet.models import Fleet


class Driver(TimeStampedModel):
    """
    Driver Model Fields

    driver_id: The unique identifier for the driver
    first_name: The first name of the driver
    last_name: The last name of the driver
    email: The email address of the driver
    phone_number: The phone number of the driver
    organization: The organization the driver belongs to
    fleet: The fleet the driver belongs to
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="drivers",
        related_query_name="driver",
        verbose_name=_("Organization"),
    )
    driver_id = models.CharField(
        _("Driver ID"), max_length=10, unique=True, null=True, blank=True
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    middle_name = models.CharField(
        _("Middle Name"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255)
    fleet = models.ManyToManyField(
        Fleet,
        blank=True,
        related_name="drivers",
        related_query_name="driver",
        verbose_name=_("Fleet"),
    )

    class Meta:
        """
        Meta Class for Driver Model

        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        ordering: The ordering of the model
        indexes: The indexes of the model
        permissions: The permissions of the model
        """

        ordering: list[functions.Lower] = (functions.Lower("last_name"),)
        verbose_name: str = _("Driver")
        verbose_name_plural: str = _("Drivers")
        indexes = [
            models.Index(fields=["-first_name"]),
        ]
        permissions = [
            ("view_all_drivers", "Can All Drivers"),
            ("search_drivers", "Can search drivers"),
        ]

    def get_driver_fleets(self):
        """
        Get the fleets for the driver

        Returns:
            list[Fleet]: The fleets for the driver
        """
        return self.fleet.all()

    def __str__(self) -> str:
        """
        String representation of the driver

        Returns:
            str: The string representation of the driver
        """
        return f"{self.driver_id} - {self.last_name}"

    def save(self, **kwargs: any) -> None:
        """
        Save the driver

        Args:
            **kwargs: Arbitrary keyword arguments
        """
        self.full_clean()
        if not self.driver_id:
            self.driver_id = (
                self.first_name[:1].upper()
                + self.last_name[:4].upper()
                + str(int(Driver.objects.count() + 1))
            )
        self.driver_id = self.driver_id.upper()
        super(Driver, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the driver

        Returns:
            str: The absolute url for the driver
        """
        return reverse("driver_edit", kwargs={"pk": self.pk})

    @property
    def get_full_name(self) -> str:
        """
        Get the full name of the driver

        Returns:
            str: The full name of the driver
        """
        return f"{self.first_name} {self.last_name}"

    def create_driver_profile(self, **kwargs) -> DriverProfile:
        """
        Create a driver profile for the driver

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            DriverProfile: The driver profile for the driver
        """
        return DriverProfile.objects.create(
            driver=self,
            address_line_1=kwargs.get("address_line_1", ""),
            address_line_2=kwargs.get("address_line_2", ""),
            city=kwargs.get("city", ""),
            state=kwargs.get("state", ""),
            zip_code=kwargs.get("zip_code", ""),
            license_number=kwargs.get("license_number", ""),
            license_state=kwargs.get("license_state", ""),
            license_expiration=kwargs.get("license_expiration", ""),
            is_hazmat=kwargs.get("is_hazmat", False),
            is_tanker=kwargs.get("is_tanker", False),
            is_double_triple=kwargs.get("is_double_triple", False),
            is_passenger=kwargs.get("is_passenger", False),
        )


class DriverProfile(TimeStampedModel):
    """
    Driver Profile Model Fields

    driver: The driver the profile belongs to
    address_line_1: The first line of the address
    address_line_2: The second line of the address
    city: The city of the address
    state: The state of the address
    zip_code: The zip code of the address
    license_number: The license number of the driver
    license_state: The state the license is issued in
    license_expiration: The expiration date of the license
    is_hazmat: Whether the driver is hazmat certified
    is_tanker: Whether the driver is tanker certified
    is_double_triple: Whether the driver is double/triple certified
    is_passenger: Whether the driver is passenger certified
    """

    driver = models.OneToOneField(
        Driver,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
        verbose_name=_("Driver"),
    )
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to="drivers/", null=True, blank=True
    )
    address_line_1 = models.CharField(
        _("Address Line 1"),
        max_length=255,
    )
    address_line_2 = models.CharField(
        _("Address Line 2"),
        max_length=255,
        null=True,
        blank=True,
    )
    city = models.CharField(
        _("City"),
        max_length=100,
    )
    state = USStateField(
        _("State"),
        help_text=_("The state the driver lives in"),
    )
    zip_code = USZipCodeField(
        _("Zip Code"),
        help_text=_("The zip code the driver lives in"),
    )
    license_number = models.CharField(
        _("License Number"),
        max_length=100,
    )
    license_state = USStateField()
    license_expiration = models.DateField(
        _("License Expiration"),
    )
    is_hazmat = models.BooleanField(
        _("Is Hazmat"),
        default=False,
    )
    is_tanker = models.BooleanField(
        _("Is Tanker"),
        default=False,
    )
    is_double_triple = models.BooleanField(
        _("Is Doubles / Triples"),
        default=False,
    )
    is_passenger = models.BooleanField(
        _("Is Passenger"),
        default=False,
    )

    class Meta:
        """
        Meta Class for Driver Profile Model

        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        """

        verbose_name: str = _("Driver Profile")
        verbose_name_plural: str = _("Driver Profiles")

    def __str__(self) -> str:
        """
        String representation of the driver profile

        Returns:
            str: The string representation of the driver profile
        """
        return f"Driver Profile for {self.driver}"

    def save(self, *args, **kwargs) -> None:
        """
        Save the driver profile

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            DriverProfile: The driver profile
        """
        self.full_clean()
        super(DriverProfile, self).save(**kwargs)

    @property
    def get_driver_full_address(self) -> str:
        """
        Get the full address of the driver

        Returns:
            str: The full address of the driver
        """
        return f"{self.address_line_1} {self.address_line_2} {self.city} {self.state} {self.zip_code}"

    def get_driver_profile_pic(self) -> str:
        """
        Get the profile picture of the driver

        Returns:
            str: The profile picture of the driver
        """
        if self.profile_picture:
            return self.profile_picture.url
        return static("media/avatars/blank.avif")


class DriverContact(TimeStampedModel):
    """
    Driver Contact Model Fields

    driver: The driver the contact belongs to
    contact_name: The name of the contact
    contact_email: The email of the contact
    contact_phone: The phone number of the contact
    is_primary: Whether the contact is the primary contact
    is_emergency: Whether the contact is an emergency contact
    """

    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="contacts",
        related_query_name="contact",
        verbose_name=_("Driver"),
    )
    contact_name = models.CharField(_("Contact Name"), max_length=255)
    contact_email = models.EmailField(
        _("Contact Email"), max_length=255, null=True, blank=True
    )
    contact_phone = models.CharField(
        _("Contact Phone"),
        max_length=10,
        null=True,
        blank=True,
    )
    is_primary = models.BooleanField(
        _("Is Primary"),
        default=False,
    )
    is_emergency = models.BooleanField(
        _("Is Emergency"),
        default=False,
    )

    class Meta:
        """
        Meta Class for Driver Contact Model

        ordering: The ordering of the driver contacts
        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        indexes: The indexes for the model
        """

        ordering: list[str] = ["driver", "contact_name"]
        verbose_name: str = _("Driver Contact")
        verbose_name_plural: str = _("Driver Contacts")
        indexes = [
            models.Index(fields=["driver", "contact_name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the driver contact

        Returns:
            str: The string representation of the driver contact
        """
        return f"Contact {self.contact_name} for {self.driver}"

    def clean(self) -> None:
        """
        Clean the driver contact

        Raises:
            ValidationError: If the contact is both primary and emergency

        Returns:
            None
        """
        # If the contact is primary, make sure there is only one primary contact
        if self.is_primary:
            if self.driver.contacts.filter(is_primary=True).exists():
                raise ValidationError(
                    _("There can only be one primary contact per driver")
                )

        # If the contact is emergency, make sure there is only one emergency contact
        if self.is_emergency:
            if self.driver.contacts.filter(is_emergency=True).exists():
                raise ValidationError(
                    _("There can only be one emergency contact per driver")
                )

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the driver contact

        Returns:
            str: The absolute url for the driver contact
        """
        return reverse("driver-contact", kwargs={"pk": self.pk})

    @property
    def get_full_contact_info(self) -> str:
        """
        Get the full contact information for the contact

        Returns:
            str: The full contact information for the contact
        """
        return f"{self.contact_name} {self.contact_email} {self.contact_phone}"


class DriverQualification(TimeStampedModel):
    """
    Driver Qualification Model Fields

    driver: The driver the qualification belongs to
    doc_class: The document class of the qualification
    name: The name of the qualification
    description: The description of the qualification
    dq_file: The file for the qualification
    dq_file_size: The size of the file for the qualification
    """

    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="driver_qualifications",
        related_query_name="driver_qualification",
        verbose_name=_("Driver"),
    )
    doc_class = models.ForeignKey(
        DocumentClassification,
        on_delete=models.PROTECT,
        related_name="driver_qualifications",
        related_query_name="driver_qualification",
        verbose_name=_("Document Classification"),
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
    )
    dq_file = models.FileField(
        _("Driver Qualification File"),
        upload_to="drivers/qualification",
    )
    dq_file_size = models.PositiveIntegerField(
        _("Driver Qualification File Size"), null=True, blank=True
    )

    class Meta:
        """
        Meta Class for Driver Qualification Model

        ordering: The ordering of the driver qualifications
        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        indexes: The indexes for the model
        """

        ordering: list[str] = ["driver", "doc_class"]
        verbose_name: str = _("Driver Qualification")
        verbose_name_plural: str = _("Driver Qualifications")
        indexes = [
            models.Index(fields=["driver", "doc_class"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the driver qualification

        Returns:
            str: The string representation of the driver qualification
        """
        return f"{self.name} with doc class {self.doc_class} for {self.driver}"

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the driver qualification

        Returns:
            str: The absolute url for the driver qualification
        """
        return reverse("driver-qualification", kwargs={"pk": self.pk})

    def get_dq_file_size(self) -> str:
        """
        Get the size of the driver qualification file

        Returns:
            str: The size of the driver qualification file
        """
        return f"{self.dq_file_size} bytes"


class CommentType(TimeStampedModel):
    """
    Comment Type Model Fields

    name: The name of the comment type
    description: The description of the comment type
    """

    name = models.CharField(_("Name"), max_length=255, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        """
        Meta Class for Comment Type Model

        ordering: The ordering of the comment types
        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        indexes: The indexes for the model
        """

        ordering: list[str] = ["name"]
        verbose_name: str = _("Comment Type")
        verbose_name_plural: str = _("Comment Types")
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str | None:
        """
        String representation of the comment type

        Returns:
            str: The string representation of the comment type
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the comment type

        Returns:
            str: The absolute url for the comment type
        """
        return reverse("comment-type", kwargs={"pk": self.pk})


class DriverComment(TimeStampedModel):
    """
    Driver Comment Model Fields

    driver: The driver the comment belongs to
    comment_type: The type of the comment
    comment: The comment
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="driver_comments",
        related_query_name="driver_comment",
        verbose_name=_("Organization"),
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="driver_comments",
        related_query_name="driver_comment",
        verbose_name=_("Driver"),
    )
    comment_type = models.ForeignKey(
        CommentType,
        on_delete=models.PROTECT,
        related_name="comments",
        related_query_name="comment",
        verbose_name=_("Comment Type"),
    )
    comment = models.TextField(_("Comment"), null=True, blank=True)

    class Meta:
        """
        Meta Class for Driver Comment Model

        ordering: The ordering of the driver comments
        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        indexes: The indexes for the model

        Returns:
            DriverComment: The driver comment
        """

        ordering: list[str] = ["driver", "comment_type"]
        verbose_name: str = _("Driver Comment")
        verbose_name_plural: str = _("Driver Comments")
        indexes = [models.Index(fields=["driver", "comment_type"])]

    def __str__(self) -> str:
        """
        String representation of the driver comment

        Returns:
            str: The string representation of the driver comment
        """
        return f"{self.driver} {self.comment_type}"

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the driver comment

        :return:  str: The absolute url for the driver comment
        :rtype:  str
        """
        return reverse("driver-comment", kwargs={"pk": self.pk})


class DriverHour(TimeStampedModel):
    """
    Driver Hour Model Fields

    driver: The driver the hours belong to
    eight_hour_clock: The eight-hour clock
    eleven_hour_clock: The eleven-hour clock
    fourteen_hour_clock: The fourteen-hour clock
    seventy_hour_clock: The seventy-hour clock
    violation_time: The violation time
    consecutive_time_off: The consecutive time off
    last_known_duty_status: The last known duty status
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="driver_hours",
        related_query_name="driver_hour",
        verbose_name=_("Organization"),
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="driver_hours",
        related_query_name="driver_hour",
        verbose_name=_("Driver"),
    )
    eight_hour_clock = models.IntegerField(
        _("Eight Hour Clock"),
        null=True,
        blank=True,
        help_text=_("The eight hour clock for the driver"),
    )
    eleven_hour_clock = models.IntegerField(
        _("Eleven Hour Clock"),
        null=True,
        blank=True,
        help_text=_("The number of hours the driver has worked in the last 11 hours"),
    )
    fourteen_hour_clock = models.IntegerField(
        _("14 Hour Clock"),
        null=True,
        blank=True,
        help_text=_("The number of hours the driver has worked in the last 14 hours"),
    )
    seventy_hour_clock = models.IntegerField(
        _("70 Hour Clock"),
        null=True,
        blank=True,
        help_text=_("The number of hours the driver has worked in the last 70 hours"),
    )
    violation_time = models.IntegerField(
        _("Violation Time"),
        null=True,
        blank=True,
        help_text=_(
            "The number of hours the driver has worked in violation of the hours of service"
        ),
    )
    consecutive_time_off = models.IntegerField(
        _("Consecutive Time Off"),
        null=True,
        blank=True,
        help_text=_(
            "The number of hours the driver has been off duty or the sleeper berth"
        ),
    )
    last_known_duty_status = models.CharField(
        _("Last Known Duty Status"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The last known duty status of the driver"),
    )

    class Meta:
        """
        Meta Class for Driver Hour Model

        ordering: The ordering of the driver hours
        verbose_name: The verbose name for the model
        verbose_name_plural: The plural verbose name for the model
        indexes: The indexes for the model
        """

        ordering: list[str] = ["driver"]
        verbose_name: str = _("Driver Hour")
        verbose_name_plural: str = _("Driver Hours")
        indexes = [
            models.Index(fields=["driver"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the driver hour

        Returns:
            str: The string representation of the driver hour
        """
        return f"{self.driver} {self.last_known_duty_status}"

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the driver hour

        Returns:
            str: The absolute url for the driver hour
        """
        return reverse("driver_hour", kwargs={"pk": self.pk})
