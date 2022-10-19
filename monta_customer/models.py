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
from typing import Any, Optional

# Core Django Models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Third Party Imports
from localflavor.us.models import USStateField, USZipCodeField
from django_extensions.db.models import TimeStampedModel

# Monta Imports
from monta_user.models import Organization


class CustomerContactChoices(models.TextChoices):
    """
    Status choices for Order model
    """

    BILLING = "BILLING", _("Billing")
    DISPATCH = "DISPATCH", _("Dispatch")
    HUMAN_RESOURCES = "HUMAN_RESOURCES", _("Human Resources")


class DocumentClassification(TimeStampedModel):
    """
    Document Classification Model Fields

    organization: The organization that the classification belongs to
    name: The name of the classification
    description: The description of the classification
    """

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        """
        Document Classification Model Meta

        ordering: The default ordering of the model
        verbose_name: The verbose name of the model
        verbose_name_plural: The plural verbose name of the model
        """

        ordering = ["name"]
        verbose_name = _("Document Classification")
        verbose_name_plural = _("Document Classifications")

    def __str__(self) -> str:
        """
        Return the string representation of the classification

        :return: The string representation of the classification
        :rtype: str
        """
        return self.name

    def save(self, **kwargs: Any) -> None:
        """
        Save the document classification object

        :param kwargs: The keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        self.name = self.name.upper()
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Return the absolute url of the classification

        :return: The absolute url of the classification
        """
        return reverse("document-classification", kwargs={"pk": self.pk})


class Customer(TimeStampedModel):
    """
    Customer Model Fields

    organization: The organization that the customer belongs to
    customer_id: The customer id of the customer
    name: The name of the customer
    customer_id: The customer id of the customer
    address_line_1: The first line of the address of the customer
    address_line_2: The second line of the address of the customer
    city: The city of the customer
    state: The state of the customer
    zip_code: The zip code of the customer
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="customers",
        related_query_name="customer",
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Is this customer active?"),
    )
    customer_id = models.SlugField(
        _("Customer ID"),
        max_length=255,
        unique=True,
        help_text="Customer ID",
        null=True,
        blank=True,
    )
    name = models.CharField(_("Name"), max_length=255)
    address_line_1 = models.CharField(_("Address Line 1"), max_length=255)
    address_line_2 = models.CharField(
        _("Address Line 2"), max_length=255, blank=True, null=True
    )
    city = models.CharField(_("City"), max_length=255)
    state = USStateField(_("State"), max_length=2)
    zip_code = USZipCodeField(_("Zip Code"), max_length=5)

    class Meta:
        ordering = ["customer_id"]
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        indexes = [
            models.Index(fields=["customer_id"]),
        ]

    def __str__(self) -> Optional[str]:
        """
        Return the string representation of the customer

        :return: The string representation of the customer
        :rtype: str
        """
        return self.customer_id

    def save(self, **kwargs: Any) -> None:
        """
        Save the customer object
        :param kwargs
        :type kwargs: Any
        :rtype: None
        """
        if not self.customer_id:
            self.customer_id = slugify(self.name)
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Return the absolute url of the customer

        :return: The absolute url of the customer
        :rtype: str
        """
        return reverse("customer_detail", kwargs={"pk": self.pk})


class CustomerBillingProfile(TimeStampedModel):
    """
    Customer Billing Profile Model Fields

    organization: The organization that the customer belongs to
    customer: The customer that the billing profile belongs to
    name: The name of the billing profile
    document_class: The document classification that the billing profile belongs to

    ------------------------------------------------------------
    Note: Model responsible for defining the Billing requirements for a specific customer
    ------------------------------------------------------------
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="billing_profiles",
        related_query_name="billing_profile",
        verbose_name=_("Organization"),
        help_text=_("Organization"),
    )
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True,
        help_text=_("Name"),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="billing_profiles",
        related_query_name="billing_profile",
        verbose_name=_("Customer"),
        help_text=_("Customer"),
    )
    document_class = models.ManyToManyField(
        DocumentClassification,
        related_name="billing_profiles",
        related_query_name="billing_profile",
        verbose_name=_("Document Classifications"),
        help_text=_("Required Document Classifications"),
    )

    class Meta:
        """
        Metaclass for the CustomerBillingProfile model

        ordering: Order by name
        verbose_name: Singular name for the model
        verbose_name_plural: Plural name for the model
        indexes: Indexes for the model
        """

        ordering = ["name"]
        verbose_name = _("Customer Billing Profile")
        verbose_name_plural = _("Customer Billing Profiles")
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Customer Billing Profile

        :return: The string representation of the Customer Billing Profile
        :rtype: str
        """
        return self.name

    def save(self, **kwargs: Any) -> None:
        """
        Save the Customer Billing Profile

        :param kwargs: Arbitrary keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.name = self.name.upper()
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the Customer Billing Profile

        :return: The absolute url for the Customer Billing Profile
        :rtype: str
        """
        return reverse("customer-billing-profile", kwargs={"pk": self.pk})


class CustomerContact(TimeStampedModel):
    """
    Customer Contact Model Fields

    organization: The organization that the customer belongs to
    customer: The customer that the contact belongs to
    name: The name of the contact
    email: The email address of the contact
    phone: The phone number of the contact
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="contacts",
        related_query_name="contact",
        verbose_name=_("Organization"),
        help_text=_("Organization"),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="contacts",
        related_query_name="contact",
        verbose_name=_("Customer"),
        help_text=_("Customer"),
    )
    contact_name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name"),
    )
    contact_email = models.EmailField(
        _("Email"),
        max_length=255,
        help_text=_("Email"),
    )
    contact_phone = models.CharField(
        _("Phone"),
        max_length=10,
        help_text=_("Phone"),
        null=True,
        blank=True,
    )
    fax_number = models.PositiveIntegerField(
        _("Fax Number"),
        help_text=_("Fax Number"),
        null=True,
        blank=True,
    )
    primary_contact = models.BooleanField(
        _("Is Primary"),
        default=False,
    )

    class Meta:
        """
        Metaclass for the CustomerContact model

        ordering: Order by contact name
        verbose_name: Singular name for the model
        verbose_name_plural: Plural name for the model
        indexes: Indexes for the model
        """

        ordering = ["contact_name"]
        verbose_name = _("Customer Contact")
        verbose_name_plural = _("Customer Contacts")
        indexes = [
            models.Index(fields=["contact_name"]),
        ]

    def clean(self) -> None:
        """
        Clean the CustomerContact model

        :return: None
        """
        if self.primary_contact:
            if self.customer.contacts.filter(primary_contact=True).exists():
                raise ValidationError(
                    _("You can only have one primary contact per customer")
                )

    def __str__(self) -> str:
        """
        String representation of the CustomerContact model

        :return: The string representation of the CustomerContact model
        :rtype: str
        """
        return self.contact_name

    def save(self, **kwargs: Any) -> None:
        """
        Save the CustomerContact model

        :param kwargs: Arbitrary keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the CustomerContact model

        :return: The absolute url for the CustomerContact model
        :rtype: str
        """
        return reverse("customer-contact", kwargs={"pk": self.pk})
