# -*- coding: utf-8 -*-
import factory

from monta_order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    """
    Order factory class
    """

    class Meta:
        model = Order

    organization = factory.SubFactory(
        "monta_organization.factories.organization.OrganizationFactory"
    )
    order_id = factory.Faker("pyint")
    status = "AVAILABLE"
