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
from __future__ import annotations
from typing import Any, final
import decimal

# Core Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.aggregates import Sum
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

# Third Party Imports
from django_extensions.db.models import TimeStampedModel
import googlemaps
import pgtrigger
from googlemaps.exceptions import ApiError

# Monta Imports
from monta_customer.models import Customer, DocumentClassification
from monta_driver.models import Driver
from monta_hazardous_material.models import HazardousMaterial
from monta_locations.models import Location
from monta_organization.models import Integration, OrganizationSettings, Organization
from monta_routes.models import Route
from monta_user.models import MontaUser
from monta_equipment.models import EquipmentType, Equipment


def order_documentation_upload_to(instance: Order, filename: str) -> str:
    """
    Upload the order documentation to the correct location.

    :param instance: The instance of the order.
    :type instance: Order
    :param filename: The name of the file.
    :type filename: str
    :return: The path to the file.
    :rtype: str
    """
    return f"order_documentation/{instance.order_id}/{filename}"


@final
class StatusChoices(models.TextChoices):
    """
    Status choices for Order model
    """

    AVAILABLE = "AVAILABLE", _("Available")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    COMPLETED = "COMPLETED", _("Completed")
    CANCELLED = "CANCELLED", _("Cancelled")


@final
class StopChoices(models.TextChoices):
    """
    Stop choices for Order model
    """

    PICKUP = "PICKUP", _("Pickup")
    SPLIT_PICKUP = "SPLIT_PICKUP", _("Split Pickup")
    SPLIT_DROP_OFF = "SPLIT_DROP_OFF", _("Split Drop Off")
    DELIVERY = "DELIVERY", _("Delivery")
    DROP_OFF = "DROP_OFF", _("Drop Off")


@final
class RateMethodChoices(models.TextChoices):
    """
    Rate method choices for Order model
    """

    FLAT = "FLAT", _("Flat")
    PER_MILE = "PER_MILE", _("Per Mile")
    PER_STOP = "PER_STOP", _("Per Stop")
    POUNDS = "POUNDS", _("Pounds")


class DelayCode(TimeStampedModel):
    """
    Delay Code Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="delay_codes",
        verbose_name=_("Organization"),
    )
    delay_code_id = models.SlugField(
        _("Delay Code ID"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name"),
        unique=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Description"),
        blank=True,
        null=True,
    )

    class Meta:
        """
        Metaclass for DelayCode model
        """

        verbose_name = _("Delay Code")
        verbose_name_plural = _("Delay Codes")
        ordering = ("delay_code_id", "name")
        indexes = [
            models.Index(fields=["delay_code_id", "name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the delay code.

        :return: The name of the delay code.
        :rtype: str
        """
        return f"{self.delay_code_id} - {self.name}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the delay code.

        :param kwargs: Keyword arguments.
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.delay_code_id:
            self.delay_code_id = slugify(self.name)
        self.name = self.name.upper()
        super(DelayCode, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the delay code.

        :return: The absolute url for the delay code.
        :rtype: str
        """
        return reverse("delay_code_detail", kwargs={"pk": self.pk})


class Commodity(TimeStampedModel):
    """
    Commodity Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="commodities",
        verbose_name=_("Organization"),
    )
    commodity_id = models.SlugField(
        _("Commodity ID"),
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name"),
        unique=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Description"),
        blank=True,
        null=True,
    )
    is_hazardous = models.BooleanField(
        _("Is Hazmat"),
        help_text=_("Is Hazmat"),
        default=False,
    )
    hazmat_class = models.ForeignKey(
        HazardousMaterial,
        on_delete=models.CASCADE,
        related_name="commodities",
        verbose_name=_("Hazardous Class"),
        blank=True,
        null=True,
    )

    class Meta:
        """
        Metaclass for the commodity model.
        """

        verbose_name = _("Commodity")
        verbose_name_plural = _("Commodities")
        ordering = ("commodity_id", "name")
        indexes = [
            models.Index(fields=["commodity_id", "name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the commodity.

        :return: The name of the commodity.
        :rtype: str
        """
        return f"{self.commodity_id} - {self.name}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the commodity.

        :param kwargs: Keyword arguments.
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.commodity_id:
            self.commodity_id = slugify(self.name)
        self.name = self.name.upper()
        super(Commodity, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the commodity.

        :return: The absolute url for the commodity.
        :rtype: str
        """
        return reverse("commodity_detail", kwargs={"pk": self.pk})


class OrderType(TimeStampedModel):
    """
    Order Type Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        related_name="order_types",
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
    )
    order_type_id = models.SlugField(
        _("Order Type ID"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Order Type ID"),
    )
    name = models.CharField(_("Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta:
        """
        Metaclass for the Order Type model.
        """

        verbose_name = _("Order Type")
        verbose_name_plural = _("Order Types")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Order Type

        :return: The name of the Order Type
        :rtype: str
        """
        return f"{self.order_type_id} - {self.name}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the Order Type

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if not self.order_type_id:
            self.order_type_id = slugify(self.name)
        super(OrderType, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the Order Type

        :return: The absolute url of the Order Type
        :rtype: str
        """
        return reverse("order_type_detail", kwargs={"pk": self.pk})


class Order(TimeStampedModel):
    """
    Order Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Organization"),
    )
    order_id = models.CharField(
        _("Order ID"),
        max_length=10,
        unique=True,
        help_text=_("Order ID"),
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
    )
    revenue_code = models.ForeignKey(
        "RevenueCode",
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Revenue Code"),
        blank=True,
        null=True,
        help_text=_("Revenue Code"),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Customer"),
    )
    pieces = models.PositiveIntegerField(
        _("Pieces"),
        help_text=_("Total Pieces"),
        default=0,
        null=True,
        blank=True,
    )
    weight = models.PositiveIntegerField(
        _("Weight"),
        help_text=_("Total Weight"),
        default=0,
        null=True,
        blank=True,
    )
    origin_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="origin_orders",
        related_query_name="order",
        verbose_name=_("Origin Location"),
    )
    origin_address = models.CharField(
        _("Origin Address"),
        max_length=255,
        null=True,
        blank=True,
    )
    origin_appointment_time = models.DateTimeField(
        _("Origin Appointment Time"),
        help_text=_(
            "The time the equipment is expected to arrive at the origin/pickup."
        ),
    )
    destination_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="destination_orders",
        related_query_name="order",
        verbose_name=_("Destination Location"),
    )
    destination_address = models.CharField(
        _("Destination Address"),
        max_length=255,
        null=True,
        blank=True,
    )
    destination_appointment_time = models.DateTimeField(
        _("Destination Appointment Time"),
        help_text=_("The time the equipment is expected to arrive at the destination."),
    )
    mileage = models.DecimalField(
        _("Total Mileage"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Total Mileage"),
    )
    other_charge_amount = models.DecimalField(
        _("Additional Charge Amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Additional Charge Amount"),
    )
    freight_charge_amount = models.DecimalField(
        _("Freight Charge Amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Freight Charge Amount"),
    )
    rate_method = models.CharField(
        _("Rating Method"),
        max_length=20,
        choices=RateMethodChoices.choices,
        default=RateMethodChoices.FLAT,
        help_text=_("Rating Method"),
    )
    comment = models.TextField(
        _("Planning Comment"),
        null=True,
        blank=True,
        help_text=_("Planning Comment"),
    )
    sub_total = models.DecimalField(
        _("Sub Total Amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Sub Total Amount"),
    )
    bill_date = models.DateField(
        _("Billed Date"),
        null=True,
        blank=True,
        help_text=_("Billed Date"),
    )
    user = models.ForeignKey(
        MontaUser,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("User"),
        help_text=_("Order entered by User"),
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Equipment Type"),
        help_text=_("Equipment Type"),
    )
    order_type = models.ForeignKey(
        OrderType,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Order Type"),
    )
    commodity = models.ForeignKey(
        Commodity,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Commodity"),
    )
    ready_to_bill = models.BooleanField(
        _("Ready to Bill"),
        default=False,
        help_text=_("Ready to Bill"),
    )
    billed = models.BooleanField(
        _("Billed"),
        default=False,
        help_text=_("Billed"),
    )
    transferred_to_billing = models.BooleanField(
        _("Transferred to Billing"),
        default=False,
        help_text=_("Transferred to Billing"),
    )
    billing_transfer_date = models.DateTimeField(
        _("Billing Transfer Date"),
        null=True,
        blank=True,
        help_text=_("Billing Transfer Date"),
    )
    hazmat_id = models.ForeignKey(
        HazardousMaterial,
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
        verbose_name=_("Hazardous Class"),
        null=True,
        blank=True,
        help_text=_("Hazardous Class"),
    )
    temperature_min = models.DecimalField(
        _("Minimum Temperature"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Minimum Temperature"),
    )
    temperature_max = models.DecimalField(
        _("Maximum Temperature"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Maximum Temperature"),
    )
    bol_number = models.CharField(
        _("BOL Number"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("BOL Number"),
    )
    consignee_ref_num = models.CharField(
        _("Consignee Reference Number"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Consignee Reference Number"),
    )

    class Meta:
        """
        Metaclass for the Order model.
        """

        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["order_id"]
        indexes = [
            models.Index(fields=["order_id"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Order

        :return: Order ID & Customer Name
        :rtype: str
        """
        return f"{self.order_id} - {self.customer.name}"

    def generate_order_id(self) -> str:
        """
        Generate Order ID

        :return: Order ID
        :rtype: str
        """
        last_order = self.objects.filter(organization=self.organization).last()
        if last_order:
            order_id = last_order.order_id
            order_id = order_id[1:]
            order_id: int = int(order_id) + 1
            new_order_id: str = "S" + str(order_id)
        else:
            new_order_id = "S1"
        return new_order_id

    def create_stops(self) -> tuple:
        """
        Create stops for the order.

        :return: Tuple of stops
        :rtype: tuple
        """

        origin_stop = Stop.objects.create(
            organization=self.organization,
            movement=self.movements.first(),
            stop_type=StopChoices.PICKUP,
            location=self.origin_location,
            address_line=self.origin_address,
            appointment_time=self.origin_appointment_time,
        )
        destination_stop = Stop.objects.create(
            organization=self.organization,
            movement=self.movements.first(),
            stop_type=StopChoices.DELIVERY,
            location=self.destination_location,
            address_line=self.destination_address,
            appointment_time=self.destination_appointment_time,
        )

        return origin_stop, destination_stop

    def create_movement(self) -> None:
        """
        Function to create movement for the order.

        :return: None
        :rtype: None
        """
        Movement.objects.create(
            organization=self.organization,
            order=self,
        )
        self.create_stops()

    def get_or_create_route(self) -> ApiError | Any:
        """
        Function to get or create route for the order.

        **********************************************************************************************************************
        * NOTE: If the Organization does not have generated routes active, and a Google api key is not provided, the
        function will not create a route. *
        **********************************************************************************************************************

        :return: Distance of the route
        :rtype: decimal.Decimal

        """
        # Check if the organization has generating routes enabled
        organization_settings = OrganizationSettings.objects.filter(
            organization__exact=self.organization,
        ).get()
        if organization_settings.generate_routes is True:
            # Check if the route already exists
            route = Route.objects.filter(
                organization=self.organization,
                origin=self.origin_location.location_id,
                destination=self.destination_location.location_id,
            ).first()
            if route:
                # If the route already exists return the distance
                return route.distance
            else:
                # Otherwise run the process of creating the route
                # Get the API key from the Integration model
                integration_api = (
                    Integration.objects.filter(
                        organization=self.organization,
                        name__exact="google_maps",
                        is_active=True,
                    )
                    .first()
                    .api_key
                )
                if integration_api:
                    # If the API key exists, start the process of creating the route
                    try:
                        gmaps = googlemaps.Client(key=integration_api)
                    except googlemaps.exceptions.ApiError as ApiError:
                        return ApiError

                    # Call the Google Maps Distance Matrix API to get the distance between the two stops.
                    direction_result = gmaps.distance_matrix(
                        origins=self.origin_location.get_address_combination,
                        destinations=self.destination_location.get_address_combination,
                        mode="driving",
                        departure_time="now",
                        language=organization_settings.language,
                        units=organization_settings.mileage_unit,
                        traffic_model=organization_settings.traffic_model,
                    )

                    print(direction_result)
                    # Create the route and return the distance.
                    created_route = Route.objects.create(
                        organization=self.organization,
                        origin=self.origin_location.location_id,
                        destination=self.destination_location.location_id,
                        distance=direction_result["rows"][0]["elements"][0]["distance"][
                            "text"
                        ].split(" ")[0],
                        # duration=direction_result["rows"][0]["elements"][0]["duration"][
                        #     "text"
                        # ].split(" ")[0],
                    )
                    return created_route.distance

    def calculate_total(self) -> decimal.Decimal:
        """
        Function to calculate the total for the order.

        :return: Total for the order
        :rtype: decimal.Decimal
        """
        if self.rate_method == RateMethodChoices.FLAT:
            if self.other_charge_amount:
                self.sub_total = self.freight_charge_amount + self.other_charge_amount
            else:
                self.sub_total = self.freight_charge_amount
            return self.sub_total
        if self.rate_method == RateMethodChoices.PER_MILE:
            if self.other_charge_amount:
                self.sub_total = (
                        self.freight_charge_amount * self.mileage + self.other_charge_amount
                )
            else:
                self.sub_total = self.freight_charge_amount * self.mileage
            return self.sub_total

    def total_pieces(self) -> int:
        """
        get the pieces for the order.

        :return: Pieces for the order
        :rtype: int
        """
        return Stop.objects.filter(movement__order__exact=self).aggregate(
            Sum("pieces")
        )["pieces__sum"]

    def total_weight(self) -> int:
        """
        Get the weight for the order.

        :return: Weight for the order
        :rtype: int
        """
        return Stop.objects.filter(movement__order__exact=self).aggregate(
            Sum("weight")
        )["weight__sum"]

    def clean(self) -> None:
        """
        Clean the Order model.

        :return: None
        :rtype: None
        :raises ValidationError
        """
        # If the rate method for the order if flat, and the charge amount is not set, raise an error.
        if self.rate_method == RateMethodChoices.FLAT:
            if self.freight_charge_amount is None:
                raise ValidationError(
                    _("Freight Charge Amount is required for flat rating method.")
                )

        # If the rate method for the order is mileage, and the mileage rate is not set, raise an error.
        if self.rate_method == RateMethodChoices.PER_MILE:
            if self.mileage is None:
                raise ValidationError(
                    _("Mileage is required for per mile rating method")
                )

        if self.ready_to_bill:
            # if the order is marked ready to bill, but the order status is not complete, raise an error.
            if self.status != StatusChoices.COMPLETED:
                raise ValidationError(
                    _(
                        "Cannot mark an order ready to bill if the order status is not complete"
                    )
                )

    def save(self, **kwargs: Any) -> None:
        """
        Save the Order

        :param kwargs: Any
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        if not self.order_id:
            # If the order ID is not set, generate one.
            self.order_id = self.generate_order_id()

        self.full_clean()

        self.origin_address = f"{self.origin_location.get_address_combination}"
        self.destination_address = (
            f"{self.destination_location.get_address_combination}"
        )

        # If the order status is complete, add the piece and weight from each stop to the order.
        if self.status == StatusChoices.COMPLETED:
            # Only total the pieces and weight if the existing total is not set.
            if self.pieces and self.weight is None:
                self.pieces = self.total_pieces()
                self.weight = self.total_weight()

        if self.ready_to_bill:
            self.sub_total = self.calculate_total()

        if self.origin_location and self.destination_location:
            # If the origin and destination locations are set, get the distance between the two stops.
            # Users can override the distance if they want.
            if self.mileage is None:
                # If the mileage is none, get the distance between the two stops.
                self.mileage = self.get_or_create_route()
        super(Order, self).save(**kwargs)
        if not self.movements.exists():
            self.create_movement()

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the order.

        :return: Absolute url for the order
        :rtype: str
        """
        return reverse("order_detail", kwargs={"pk": self.pk})


class Movement(TimeStampedModel):
    """
    Movement Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="movements",
        related_query_name="movement",
        verbose_name=_("Organization"),
    )
    assigned_driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name="movements",
        related_query_name="movement",
        verbose_name=_("Assigned Driver"),
        null=True,
        blank=True,
    )
    assigned_driver_2 = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name="movements_two",
        related_query_name="movement_two",
        verbose_name=_("Assigned Driver 2"),
        null=True,
        blank=True,
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name="movements",
        related_query_name="movement",
        verbose_name=_("Equipment"),
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="movements",
        related_query_name="movement",
        verbose_name=_("Order"),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
    )

    class Meta:
        """
        Metaclass for Movement Model
        """

        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Movement

        :return: String representation of the Movement
        :rtype: str
        """
        return f"{self.order} - {self.assigned_driver}"

    def sequence_stops(self) -> None:
        """
        Set the stop sequence number for the stops in the movement based on when the stops were created.

        :return: None
        :rtype: None
        """
        # If the sequence is not ordered currently order it.
        # add to fix maximum recursion depth exceeded in comparison
        if (
                not self.stops.order_by("sequence")
                            .values_list("sequence", flat=True)
                            .distinct()
                            .count()
                    == self.stops.count()
        ):
            stops = self.stops.order_by("created")
            for index, stop in enumerate(stops, start=1):
                stop.sequence = index
                stop.save()

    def clean(self) -> None:
        """
        Clean the Movement object

        :return: None
        :rtype: None
        :raises ValidationError
        """
        if self.status == StatusChoices.AVAILABLE:
            if self.pk:
                old_status = Movement.objects.get(pk=self.pk).status
                # If the movement status is changed from available to something else, raise an error.
                if (
                        old_status == StatusChoices.IN_PROGRESS
                        or old_status == StatusChoices.COMPLETED
                ):
                    raise ValidationError(
                        _("Movement status cannot be changed back to available")
                    )

        # If the status is in progress, make sure the assigned driver & equipment is set.
        elif self.status == StatusChoices.IN_PROGRESS:
            if self.assigned_driver is None:
                raise ValidationError(
                    _("Movement cannot be in progress without an assigned driver")
                )
            if self.equipment is None:
                raise ValidationError(
                    _("Movement cannot be in progress without an assigned equipment")
                )

        if self.pk:
            # if self.status == StatusChoices.IN_PROGRESS:
            #     if self.stops.filter(status=StatusChoices.AVAILABLE).exists():
            #         raise ValidationError(
            #             _("You can't put movement status in progress if the movement stops are not in progress.")
            #         )
            #
            # # If the movement status is changed from in progress to something else, raise an error.
            # elif self.status == StatusChoices.AVAILABLE:
            #     if self.stops.filter(status=StatusChoices.IN_PROGRESS).exists():
            #         raise ValidationError(
            #             _("You can't put movement status available if the movement stops are in progress.")
            #         )

            # If the movement status is changed from completed to something else, raise an error
            # if self.stops.filter(status=StatusChoices.COMPLETED):
            #     raise ValidationError(
            #         _(
            #             "You can't put movement status available if the movement stops are completed."
            #         )
            #     )
            #
            #  If the movement is in progress, make sure the stops are in progress.
            # if self.stops.filter(status=StatusChoices.IN_PROGRESS):
            #     raise ValidationError(
            #         _(
            #             "You can't put movement status available if the movement stops are in progress."
            #         )
            #     )

            # If the primary driver and the secondary driver are the same, raise an error.
            if self.assigned_driver == self.assigned_driver_2:
                raise ValidationError(
                    _("The primary driver and the secondary driver cannot be the same.")
                )

        super(Movement, self).clean()

    def save(self, **kwargs: Any) -> None:
        """
        Save the Movement object

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()
        if self.status == StatusChoices.IN_PROGRESS:
            self.order.status = StatusChoices.IN_PROGRESS
            self.order.save()

        if self.assigned_driver:
            self.equipment = self.assigned_driver.equipments.first()
        super(Movement, self).save(**kwargs)

        if self.status == StatusChoices.COMPLETED:
            if not self.order.movements.filter(
                    status=StatusChoices.IN_PROGRESS
            ).exists():
                self.order.status = StatusChoices.COMPLETED
                self.order.save()

        self.sequence_stops()


class ServiceIncident(TimeStampedModel):
    """
    Service Incident Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="service_incidents",
        related_query_name="service_incident",
        verbose_name=_("Organization"),
    )
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
        related_name="service_incidents",
        related_query_name="service_incident",
        verbose_name=_("Movement"),
    )
    stop = models.ForeignKey(
        "Stop",
        on_delete=models.CASCADE,
        related_name="service_incidents",
        related_query_name="service_incident",
        verbose_name=_("Stop"),
    )
    delay_code = models.ForeignKey(
        DelayCode,
        on_delete=models.PROTECT,
        related_name="service_incidents",
        related_query_name="service_incident",
        verbose_name=_("Delay Code"),
    )
    delay_reason = models.CharField(
        _("Delay Reason"),
        max_length=100,
        null=True,
        blank=True,
    )
    delay_time = models.DurationField(
        _("Delay Time"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Service Incident")
        verbose_name_plural = _("Service Incidents")
        ordering = ["movement"]
        indexes = [
            models.Index(fields=["movement"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the Service Incident

        :return: Service Incident string representation
        :rtype: str
        """
        return f"{self.movement} - {self.stop} - {self.delay_code}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the Service Incident object

        :param kwargs: Keyword arguments
        :type kwargs: Any
        """
        if not self.delay_reason:
            self.delay_reason = self.delay_code.description
        super(ServiceIncident, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the Service Incident

        :return: Absolute url for the Service Incident
        :rtype: str
        """
        return reverse("service_incident-detail", kwargs={"pk": self.pk})


class Stop(TimeStampedModel):
    """
    Stop model fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="stops",
        related_query_name="stop",
        verbose_name=_("Organization"),
        help_text=_("The organization that the stop belongs to."),
    )
    sequence = models.PositiveIntegerField(
        _("Sequence"),
        default=1,
        null=True,
        blank=True,
        help_text=_("The sequence of the stop in the movement."),
    )
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
        related_name="stops",
        related_query_name="stop",
        verbose_name=_("Movement"),
        help_text=_("The movement that the stop belongs to."),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="stops",
        related_query_name="stop",
        verbose_name=_("Location"),
        help_text=_("The location of the stop."),
    )
    pieces = models.PositiveIntegerField(
        _("Pieces"),
        default=0,
        null=True,
        blank=True,
        help_text=_("Pieces"),
    )
    weight = models.PositiveIntegerField(
        _("Weight"),
        default=0,
        null=True,
        blank=True,
        help_text=_("Weight"),
    )
    address_line = models.CharField(
        _("Stop Address"),
        max_length=255,
        help_text=_("Stop Address"),
    )
    appointment_time = models.DateTimeField(
        _("Stop Appointment Time"),
        help_text=_("The time the equipment is expected to arrive at the stop."),
    )
    arrival_time = models.DateTimeField(
        _("Stop Arrival Time"),
        null=True,
        blank=True,
        help_text=_("The time the equipment actually arrived at the stop."),
    )
    departure_time = models.DateTimeField(
        _("Stop Departure Time"),
        null=True,
        blank=True,
        help_text=_("The time the equipment actually departed from the stop."),
    )
    stop_type = models.CharField(
        max_length=20,
        choices=StopChoices.choices,
        help_text=_("The type of stop."),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE,
        help_text=_("The status of the stop."),
    )

    class Meta:
        """
        Metaclass for the Stop model
        """

        verbose_name = _("Stop")
        verbose_name_plural = _("Stops")
        ordering = ["sequence"]
        indexes = [
            models.Index(fields=["sequence"]),
        ]
        triggers = [
            pgtrigger.Protect(
                name="stops_protect_redundant_updates",
                operation=pgtrigger.Update,
                condition=pgtrigger.Condition(
                    "OLD.* IS DISTINCT FROM NEW.*",
                )
            )
        ]

    def __str__(self) -> str:
        """
        String representation of the Stop

        :return: Stop string representation
        :rtype: str
        """
        return f"{self.movement} - {self.sequence} - {self.location}"

    def clean(self) -> None:
        """
        Clean the Stop object

        :return: None
        :rtype: None
        :raises ValidationError
        """
        if self.pk:
            if self.status == StatusChoices.AVAILABLE:
                old_status = Stop.objects.get(pk__exact=self.pk).status
                if (
                        old_status == StatusChoices.IN_PROGRESS
                        or old_status == StatusChoices.COMPLETED
                ):
                    raise ValidationError(
                        _("Stop status cannot be changed back to available")
                    )

            if self.movement.assigned_driver and self.movement.equipment is None:
                raise ValidationError(
                    _(
                        "Movement must have a driver and equipment to be in progress or completed"
                    )
                )

            if self.sequence > 1:
                previous_stop = self.movement.stops.filter(
                    sequence__exact=self.sequence - 1
                ).first()
                if previous_stop:
                    if self.appointment_time < previous_stop.appointment_time:
                        raise ValidationError(
                            _(
                                "Stop appointment time cannot be before the previous stop appointment time"
                            )
                        )
                    if previous_stop.status != StatusChoices.COMPLETED:
                        if (
                                self.status == StatusChoices.IN_PROGRESS
                                or self.status == StatusChoices.COMPLETED
                        ):
                            raise ValidationError(
                                _(
                                    "The previous stop must be completed before the next stop can be put in progress "
                                    "or completed "
                                )
                            )

            if self.sequence < self.movement.stops.count():
                next_stop = self.movement.stops.filter(
                    sequence__exact=self.sequence + 1
                ).first()
                if next_stop:
                    if self.appointment_time > next_stop.appointment_time:
                        raise ValidationError(
                            _(
                                "Stop appointment time cannot be after the next stop appointment time"
                            )
                        )
                    if self.status != StatusChoices.COMPLETED:
                        if (
                                next_stop.status == StatusChoices.IN_PROGRESS
                                or next_stop.status == StatusChoices.COMPLETED
                        ):
                            raise ValidationError(
                                _(
                                    "The next stop must be available before the previous stop can be put in progress "
                                    "or completed "
                                )
                            )
            if self.movement.assigned_driver is None or self.movement.equipment is None:
                if (
                        self.status == StatusChoices.IN_PROGRESS
                        or self.status == StatusChoices.COMPLETED
                ):
                    raise ValidationError(
                        _(
                            "Movement must have a driver and equipment to be in progress or completed"
                        )
                    )
                if self.arrival_time or self.departure_time:
                    raise ValidationError(
                        _(
                            "Movement must have a driver and equipment to have arrival or departure time"
                        )
                    )

            if self.departure_time:
                if not self.arrival_time:
                    raise ValidationError(
                        _(
                            "Stop arrival time must be set before the stop departure time"
                        )
                    )
                if self.departure_time < self.arrival_time:
                    raise ValidationError(
                        _("Stop departure time cannot be before the stop arrival time")
                    )
        super(Stop, self).clean()

    def save(self, **kwargs: Any) -> None:
        """
        Save the Stop object

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        self.full_clean()

        # If the status changes to in progress, change the movement status associated to this stop to in progress.
        if self.status == StatusChoices.IN_PROGRESS:
            self.movement.status = StatusChoices.IN_PROGRESS
            self.movement.save()

        # if the last stop is completed, change the movement status to complete.
        if self.status == StatusChoices.COMPLETED:
            if (
                    self.movement.stops.filter(status=StatusChoices.COMPLETED).count()
                    == self.movement.stops.count()
            ):
                self.movement.status = StatusChoices.COMPLETED
                self.movement.save()

        # If the arrival time is set, change the status to in progress.
        if self.arrival_time:
            self.status = StatusChoices.IN_PROGRESS

        # If the stop arrival and departure time are set, change the status to complete.
        if self.arrival_time and self.departure_time:
            self.status = StatusChoices.COMPLETED

        # If the arrival time of the stop is after the appointment time, create a service incident.
        if self.arrival_time:
            if self.arrival_time > self.appointment_time:
                ServiceIncident.objects.create(
                    organization=self.movement.order.organization,
                    movement=self.movement,
                    stop=self,
                    delay_code=DelayCode.objects.filter(pk__exact=1).first(),
                    delay_time=self.arrival_time - self.appointment_time,
                )
        super(Stop, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url of the Stop object

        :return: Absolute url of the Stop object
        :rtype: str
        """
        return reverse("stop_detail", kwargs={"pk": self.pk})


class OrderDocumentation(TimeStampedModel):
    """
    Order Documentation Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="order_documentation",
        verbose_name=_("Organization"),
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_documentation",
        verbose_name=_("Order"),
    )
    document = models.FileField(
        _("Document"),
        upload_to=order_documentation_upload_to,
        null=True,
        blank=True,
    )
    document_class = models.ForeignKey(
        DocumentClassification,
        on_delete=models.CASCADE,
        related_name="order_documentation",
        verbose_name=_("Document Class"),
        help_text=_("Document Class"),
    )

    class Meta:
        """
        Metaclass for OrderDocumentation
        """

        verbose_name = _("Order Documentation")
        verbose_name_plural = _("Order Documentation")
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the OrderDocumentation

        :return: String representation of the OrderDocumentation
        :rtype: str
        """
        return f"{self.order} - {self.document_class}"

    def save(self, **kwargs: Any) -> None:
        """
        Save the OrderDocumentation object

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        super(OrderDocumentation, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        """
        Get the absolute url for the OrderDocumentation object

        :return: Absolute url for the OrderDocumentation object
        :rtype: str
        """
        return reverse("order_documentation_detail", kwargs={"pk": self.pk})


class RevenueCode(TimeStampedModel):
    """
    Revenue Code Model Fields
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        related_name="revenue_codes",
        related_query_name="revenue_code",
        verbose_name=_("Organization"),
        help_text=_("Organization that the revenue code belongs to."),
    )

    # TODO: Rename this field
    code = models.CharField(
        _("Code"),
        max_length=5,
        unique=True,
        help_text=_("Code of the Revenue Code"),
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("Description of the Revenue Code"),
    )

    class Meta:
        """
        Metaclass for Revenue Code Model
        """

        verbose_name = _("Revenue Code")
        verbose_name_plural = _("Revenue Codes")
        ordering = ["code"]

    def __str__(self) -> str:
        """
        String representation of the Revenue Code Model

        :return: String representation of the Revenue Code Model
        :rtype: str
        """
        return self.code

    def save(self, **kwargs: Any) -> None:
        """
        Save the Revenue Code Object.

        :param kwargs: Keyword arguments
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        if self.code:
            self.code = self.code.upper()
        super(RevenueCode, self).save(**kwargs)
