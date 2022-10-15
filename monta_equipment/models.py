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

# Standard library imports
from typing import Any

# Core Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from django_extensions.db.models import TimeStampedModel
from localflavor.us.models import USStateField

# Monta Imports
from monta_driver.models import Driver
from monta_user.models import Organization, MontaUser


class EquipmentType(TimeStampedModel):
    """
    Equipment Type Model Fields

    equip_type_id: Unique identifier for the equipment type
    name: Name of the equipment type
    description: Description of the equipment type
    """
    organization = models.ForeignKey(
        Organization,
        related_name="equipment_types",
        related_query_name="equipment_type",
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
    )
    equip_type_id = models.CharField(
        _("Equipment Type ID"), max_length=50, primary_key=True
    )
    name = models.CharField(_("Equipment Type Name"), max_length=50)
    description = models.CharField(
        _("Equipment Type Description"), max_length=200, blank=True, null=True
    )

    class Meta:
        """
        Equipment Type Model Metaclass
        """
        verbose_name = _("Equipment Type")
        verbose_name_plural = _("Equipment Types")
        ordering = ["equip_type_id"]
        indexes = [
            models.Index(fields=["equip_type_id"]),
        ]

    def __str__(self) -> str:
        """
        Equipment Type Model String Representation

        :return: String representation of the equipment type
        :rtype: str
        """
        return f"{self.equip_type_id} - {self.name}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Equipment Type Model Save Method

        :param args: Arguments
        :type args: Any
        :param kwargs: Keyword Arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.equip_type_id = self.equip_type_id.upper()
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Equipment Type Model Absolute URL

        :return: Absolute URL for the equipment type
        :rtype: str
        """
        return reverse("equipment_type_detail", kwargs={"pk": self.pk})


class Equipment(TimeStampedModel):
    """
    Equipment Model Fields

    organization: The organization the equipment belongs to
    is_active: Whether the equipment is active or not
    equip_id: Unique identifier for the equipment
    equipment_type: The type of equipment
    description: Description of the equipment
    vin_number: Vehicle Identification Number
    primary_driver: Primary driver of the equipment
    secondary_driver: Secondary driver of the equipment
    vehicle_model: Model of the vehicle
    vehicle_make: Make of the vehicle
    vehicle_year: Year of the vehicle
    vehicle_license_expiration: Expiration date of the vehicle license plate
    state: State the vehicle is registered in

    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="equipments",
        related_query_name="equipment",
        verbose_name=_("Organization"),
        help_text=_("The organization the equipment belongs to."),
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Whether the equipment is active or not."),
    )
    equip_id = models.CharField(
        _("Equipment ID"),
        max_length=50,
        unique=True,
        help_text=_("Unique identifier for the equipment."),
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="equipments",
        related_query_name="equipment",
        verbose_name=_("Equipment Type"),
        help_text=_("The type of equipment."),
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("Description of the equipment."),
    )
    vin_number = models.CharField(
        _("Vehicle Identification Number"),
        max_length=17,
        blank=True,
        null=True,
        help_text=_("Vehicle Identification Number."),
    )
    primary_driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="equipments",
        related_query_name="equipment",
        verbose_name=_("Primary Driver"),
        help_text=_("Primary driver of the equipment."),
    )
    secondary_driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="equipments_secondary",
        related_query_name="equipment_secondary",
        verbose_name=_("Secondary Driver"),
        blank=True,
        null=True,
        help_text=_("Secondary driver of the equipment."),
    )
    vehicle_model = models.CharField(
        _("Vehicle Model"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Model of the vehicle."),
    )
    vehicle_make = models.CharField(
        _("Vehicle Make"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Make of the vehicle."),
    )
    vehicle_year = models.DateField(
        _("Vehicle Year"),
        blank=True,
        null=True,
        help_text=_("Year of the vehicle."),
    )
    vehicle_license_expiration = models.DateField(
        _("Vehicle License Expiration"),
        blank=True,
        null=True,
        help_text=_("Expiration date of the vehicle license plate."),
    )
    state = USStateField(
        _("State"),
        help_text=_("State of the vehicle"),
    )

    class Meta:
        """
        Meta class for Equipment

        Attributes:
            verbose_name (str): verbose name for Equipment
            verbose_name_plural (str): verbose name plural for Equipment
            ordering (list): ordering for Equipment
            indexes (list): indexes for Equipment
        """

        verbose_name: str = _("Equipment")
        verbose_name_plural: str = _("Equipment")
        ordering: list[str] = ["equip_id"]
        indexes = [
            models.Index(fields=["equip_id"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the equipment object.

        :return: String representation of the equipment object
        :rtype: str
        """
        return f"{self.equip_id} - {self.vehicle_make} {self.vehicle_model}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the equipment object.

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.equip_id = self.equip_id.upper()
        super().save(**kwargs)

    def clean(self) -> None:
        """
        Clean the equipment object.

        :raises ValidationError
        :return: None
        :rtype: None
        """
        if self.secondary_driver == self.primary_driver:
            raise ValidationError(
                _("Primary and Secondary Drivers cannot be the same.")
            )

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the equipment object.

        :return: Absolute url for the equipment object
        :rtype: str
        """
        return reverse("equipment_detail", kwargs={"pk": self.pk})

    def get_make_model_year(self) -> str:
        """
        Get the make, model, and year of the equipment object.

        :return: Make, model, and year of the equipment object
        :rtype: str
        """
        return f"{self.vehicle_make} {self.vehicle_model} {self.vehicle_year}"


class EquipmentPermit(TimeStampedModel):
    """
    Equipment Permit Model Fields

    organization: The organization the equipment permit belongs to
    equipment: The equipment the permit belongs to
    name: Name of the permit
    description: Description of the permit
    user: User who created the permit
    permit_file: File of the permit
    permit_file_size: Size of the permit file
    deletion_date: Date the permit will be deleted
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="equipment_permits",
        related_query_name="equipment_permit",
        verbose_name=_("Organization"),
        help_text=_("The organization the equipment permit belongs to."),
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="equipment_permits",
        related_query_name="equipment_permit",
    )
    name = models.CharField(_("Permit Name"), max_length=50)
    description = models.CharField(
        _("Permit Description"), max_length=200, blank=True, null=True
    )
    user = models.ForeignKey(
        MontaUser,
        on_delete=models.CASCADE,
        related_name="equipment_permits",
        related_query_name="equipment_permit",
    )
    permit_file = models.FileField(_("Permit File"), upload_to="permits/")
    permit_file_size = models.PositiveIntegerField(
        _("Permit File Size"), blank=True, null=True
    )
    # Going to be used to "soft delete" the permit file.
    deletion_date = models.DateTimeField(_("Deletion Date"), blank=True, null=True)

    class Meta:
        """
        Metaclass for the EquipmentPermit model.

        Attributes:
            verbose_name: The verbose name for the EquipmentPermit model.
            verbose_name_plural: The verbose name plural for the EquipmentPermit model.
            ordering: The ordering for the EquipmentPermit model.
            indexes: The indexes for the EquipmentPermit model.
        """

        verbose_name: str = _("Equipment Permit")
        verbose_name_plural: str = _("Equipment Permits")
        ordering: list[str] = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the EquipmentPermit object.

        Returns:
            str: String representation of the EquipmentPermit object.
        """
        return f"{self.equipment} - {self.permit_file}"

    def clean(self) -> None:
        """
        Clean the EquipmentPermit object.

        :raises ValidationError
        :return: None
        :rtype: None
        """
        if self.deletion_date:
            raise ValidationError(_("Permit File cannot be deleted."))
        if self.permit_file_size:
            if self.permit_file_size > 10000000:
                raise ValidationError(_("Permit File cannot be larger than 10MB."))
        super().clean()

    def save(self, **kwargs: Any) -> None:
        """
        This is a hack to get the file size. I know it's not the best way to do it, but it works.

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.permit_file_size = self.permit_file.size / (1024 ** 2)
        super(EquipmentPermit, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the EquipmentPermit object.

        :return: Absolute url for the EquipmentPermit object
        :rtype: str
        """
        return reverse("equipment_permit_detail", kwargs={"pk": self.pk})
