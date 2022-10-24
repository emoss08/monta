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
from typing import Any, final

from django.core.exceptions import ValidationError
# Core Django Imports
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Third Party Imports
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_order.models import Order, StatusChoices
from monta_user.models import Organization


@final
class BillingExceptionChoices(models.TextChoices):
    """
    Status choices for Order model
    """

    PAPERWORK = "PAPERWORK", _("Paperwork")
    CHARGE = "CHARGE", _("Charge")
    CREDIT = "CREDIT", _("Credit")
    DEBIT = "DEBIT", _("Debit")
    OTHER = "OTHER", _("Other")


@final
class BillTypeChoices(models.TextChoices):
    """
    Status choices for Order model
    """

    INVOICE = "INVOICE", _("Invoice")
    CREDIT = "CREDIT", _("Credit")
    DEBIT = "DEBIT", _("Debit")
    PREPAID = "PREPAID", _("Prepaid")
    OTHER = "OTHER", _("Other")


class ChargeType(TimeStampedModel):
    """
    Charge Type Model Fields

    name: Name of the Charge Type
    description: Description of the Charge Type

    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="charge_types",
        related_query_name="charge_type",
        verbose_name=_("Organization"),
    )
    name = models.CharField(
        _("Name of Charge Type"),
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        _("Description of Charge Type"),
        blank=True,
        null=True,
    )

    class Meta:
        """
        Meta Class for Charge Type Model
        """

        ordering: list[str] = ["name"]
        verbose_name: str = _("Charge Type")
        verbose_name_plural: str = _("Charge Types")

    def __str__(self) -> str:
        """
        :return: String representation of the Charge Type Model
        :rtype: str
        """
        return self.name

    def save(self, **kwargs: Any) -> None:
        """
        Save the Charge Type Model

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        self.name = self.name.upper()
        if self.description:
            self.description = self.description.capitalize()
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the order.

        :return: Absolute url for the order
        :rtype: str
        """
        return reverse("charge_type_edit", kwargs={"pk": self.pk})


class AdditionalCharge(TimeStampedModel):
    """
    Additional Charge Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="additional_charges",
        related_query_name="additional_charge",
        verbose_name=_("Organization"),
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        related_name="additional_charges",
        related_query_name="additional_charge",
        verbose_name=_("Order"),
    )
    name = models.CharField(
        _("Name of the additional charge"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
    )
    charge_type = models.ForeignKey(
        ChargeType,
        on_delete=models.RESTRICT,
        related_name="additional_charges",
        related_query_name="additional_charge",
        verbose_name=_("Charge Type"),
    )
    unit = models.PositiveIntegerField(
        _("Unit"),
        default=1,
        help_text=_("Number of units of the charge"),
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Amount of the charge"),
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total amount of the additional charge",
    )

    class Meta:
        """
        Meta Class for Additional Charge Model
        """

        verbose_name: str = _("Additional Charge")
        verbose_name_plural: str = _("Additional Charges")
        ordering: list[str] = ["name"]
        indexes: list[models.Index] = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Additional Charge Model

        :return: Name of the Additional Charge
        :rtype: str
        """
        return self.name

    def save(self, **kwargs: Any) -> None:
        """
        Save the Additional Charge Object.

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.name = self.name.upper()
        self.total_amount = self.unit * self.amount
        self.order.other_charge_amount = self.total_amount
        self.order.save()
        super().save(**kwargs)


class BillingQueue(TimeStampedModel):
    """
    Billing Queue Model Fields

    ----------------------------------------
    NOTE: Intermediate model for storing order information before it is billed.
    ----------------------------------------
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="billing_queues",
        related_query_name="billing_queue",
        verbose_name=_("Organization"),
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        related_name="billing_queues",
        related_query_name="billing_queue",
        verbose_name=_("Order"),
    )
    bill_type = models.CharField(
        _("Bill Type"),
        max_length=10,
        choices=BillTypeChoices.choices,
        default=BillTypeChoices.INVOICE,
    )
    other_charge_total = models.DecimalField(
        _("Other Charge Total"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Total of all other charges on the order"),
    )
    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Total amount of the order"),
    )

    class Meta:
        """
        Meta Class for Billing Queue Model
        """

        verbose_name: str = _("Billing Queue")
        verbose_name_plural: str = _("Billing Queues")
        ordering: list[str] = ["order"]
        indexes: list[models.Index] = [
            models.Index(fields=["order"]),
        ]
        permissions: list[tuple[str, str]] = [
            ("transfer_to_billing", "Can Transfer to Billing"),
            ("bill_orders", "Can Bill Orders"),
            ("re_bill_orders", "Can Re Bill Orders"),
        ]

    def clean(self) -> None:
        """
        Clean the Billing Queue Model

        :return: None
        :rtype: None
        """
        if self.order.billed is True:
            raise ValidationError(_("Order is already billed."))
        if self.order.transferred_to_billing is True:
            raise ValidationError(_("Order is already in the billing queue."))
        if self.order.status == StatusChoices.CANCELLED:
            raise ValidationError(_("Order is already cancelled."))
        if self.order.ready_to_bill is False:
            raise ValidationError(_("Order is not marked ready to bill."))
        super().clean()

    def save(self, **kwargs: Any) -> None:
        """
        Save the Billing Queue Object.

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.bill_type:
            self.bill_type = BillTypeChoices.INVOICE
        self.total_amount = self.order.sub_total
        self.other_charge_total = self.order.other_charge_amount
        super().save(**kwargs)

    def __str__(self) -> str:
        """
        String representation of the Billing Queue Model

        :return: Name of the Billing Queue
        :rtype: str
        """
        return f"{self.organization} - {self.order}"


class BillingException(TimeStampedModel):
    """
    Billing Exception Model Fields

    ----------------------------------------
    NOTE: Model responsible for storing billing exceptions.
    ----------------------------------------
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="billing_exceptions",
        related_query_name="billing_exception",
        verbose_name=_("Organization"),
    )
    exception_type = models.CharField(
        _("Exception Type"),
        max_length=10,
        choices=BillingExceptionChoices.choices,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        related_name="billing_exceptions",
        related_query_name="billing_exception",
        verbose_name=_("Order"),
    )
    exception_message = models.TextField(
        _("Exception"),
        blank=True,
        null=True,
    )

    class Meta:
        """
        Metaclass for Billing Exception Model
        """

        verbose_name: str = _("Billing Exception")
        verbose_name_plural: str = _("Billing Exceptions")

    def __str__(self) -> str:
        """
        String representation of the Billing Exception Model

        :return: Name of the Billing Exception
        :rtype: str
        """
        return self.exception_type


class BillingHistory(TimeStampedModel):
    """
    Billing History Model Fields
    """

    batch_name = models.CharField(
        _("Batch Name"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    bill_type = models.CharField(
        _("Bill Type"),
        max_length=10,
        choices=BillTypeChoices.choices,
        default=BillTypeChoices.INVOICE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="billing_histories",
        related_query_name="billing_history",
        verbose_name=_("Organization"),
    )
    sub_total = models.DecimalField(
        _("Sub Total"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        related_name="billing_histories",
        related_query_name="billing_history",
        verbose_name=_("Order"),
    )

    class Meta:
        """
        Metaclass for Billing History Model
        """

        verbose_name: str = _("Billing History")
        verbose_name_plural: str = _("Billing Histories")
        ordering: list[str] = ["batch_name"]
        indexes: list[models.Index] = [
            models.Index(fields=["batch_name"]),
        ]

    def clean(self) -> None:
        """
        Clean the Billing History Model

        :return: None
        :rtype: None
        """
        if not self.order.billed:
            raise ValidationError(
                "Order must be marked billed before putting into the billing history."
            )
        super().clean()

    def __str__(self) -> str:
        """
        String representation of the Billing History Model

        :return: Name of the Billing History
        :rtype: str
        """
        return str(self.batch_name)

    @property
    def generate_batch_name(self) -> str:
        """
        Generate the batch name for the billing history.

        :return: Batch Name
        :rtype: str
        """
        last_batch_name: BillingHistory | None = (
            BillingHistory.objects.filter(
                organization=self.organization,
            )
            .order_by("-created")
            .first()
        )
        if last_batch_name:
            batch_name = last_batch_name.batch_name
            batch_name = batch_name[1:]
            batch_name = int(batch_name) + 1
            batch_name = f"B{batch_name}"
        else:
            batch_name = "B1"

        return batch_name

    def save(self, **kwargs: Any) -> None:
        """
        Save the Billing History Object.

        :param kwargs: Keyword Arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        self.batch_name = self.generate_batch_name
        self.sub_total = round(self.order.sub_total, 2)
        super(BillingHistory, self).save(**kwargs)
