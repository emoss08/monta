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
        verbose_name = _("Equipment Type")
        verbose_name_plural = _("Equipment Types")
        ordering = ["equip_type_id"]
        indexes = [
            models.Index(fields=["equip_type_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.equip_type_id} - {self.name}"

    def save(self, *args, **kwargs) -> None:
        self.equip_type_id = self.equip_type_id.upper()
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        return reverse("equipment_type_detail", kwargs={"pk": self.pk})


class Equipment(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="equipments",
        related_query_name="equipment",
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    equip_id = models.CharField(
        _("Equipment ID"),
        max_length=50,
        unique=True,
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="equipments",
        related_query_name="equipment",
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    vin_number = models.CharField(
        _("Vehicle Identification Number"), max_length=17, blank=True, null=True
    )
    primary_driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="equipment",
        related_query_name="equipment",
    )
    secondary_driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="secondary_driver"
    )
    vehicle_model = models.CharField(
        _("Vehicle Model"), max_length=255, blank=True, null=True
    )
    vehicle_make = models.CharField(
        _("Vehicle Make"), max_length=255, blank=True, null=True
    )
    vehicle_year = models.DateField(_("Vehicle Year"), blank=True, null=True)
    vehicle_license_expiration = models.DateField(
        _("Vehicle License Expiration"), blank=True, null=True
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

        Returns:
            str: String representation of the equipment object.
        """
        return f"{self.equip_id} - {self.vehicle_make} {self.vehicle_model}"

    def save(self, **kwargs) -> None:
        """
        Save the equipment object.

        Args:
            **kwargs: Keyword arguments to pass to the save method.

        Returns:
            None
        """
        self.equip_id = self.equip_id.upper()
        super().save(**kwargs)

    def clean(self) -> None:
        """
        Clean the equipment object.

        Raises: ValidationError

        Returns:
            None
        """
        if self.secondary_driver == self.primary_driver:
            raise ValidationError(
                _("Primary and Secondary Drivers cannot be the same.")
            )

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the equipment object.

        Returns:
            str: The absolute url for the equipment object.
        """
        return reverse("equipment_detail", kwargs={"pk": self.pk})

    def get_make_model_year(self) -> str:
        """
        Get the make, model, and year of the equipment object.

        Returns:
            str: The make, model, and year of the equipment object.
        """
        return f"{self.vehicle_make} {self.vehicle_model} {self.vehicle_year}"


class EquipmentPermit(TimeStampedModel):
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
    """
    Because Techy is a fan of soft-deletes ,but it makes sense to use soft deletes on permit files. Just incase they need to be restored.
    """
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

        Raises:
            ValidationError: If the permit file size is greater than 10MB.
        """
        if self.deletion_date:
            raise ValidationError(_("Permit File cannot be deleted."))
        if self.permit_file_size:
            if self.permit_file_size > 10000000:
                raise ValidationError(_("Permit File cannot be larger than 10MB."))
        super().clean()

    def save(self, **kwargs):
        """
        This is a hack to get the file size. I know it's not the best way to do it, but it works.

        Args:
            **kwargs: Keyword arguments
        """
        self.permit_file_size = self.permit_file.size / (1024**2)
        super(EquipmentPermit, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """Returns the url to access a particular instance of EquipmentPermit."""
        return reverse("equipment_permit_detail", kwargs={"pk": self.pk})
