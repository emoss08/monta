# -*- coding: utf-8 -*-
import factory

from monta_customer.models import (
    Customer,
    DocumentClassification,
    CustomerBillingProfile,
    CustomerContact,
)


class DocumentClassificationFactory(factory.django.DjangoModelFactory):
    """
    DocumentClassifications factory class
    """

    class Meta:
        model = DocumentClassification

    name = factory.Faker("name")
    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    description = factory.Faker("text")


class CustomerFactory(factory.django.DjangoModelFactory):
    """
    Customer factory class
    """

    class Meta:
        model = Customer

    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    is_active = factory.Faker("boolean")
    name = factory.Faker("name")
    address_line_1 = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip_code = factory.Faker("zipcode")


class CustomerBillingProfileFactory(factory.django.DjangoModelFactory):
    """
    Customer Billing Profile factory class
    """

    class Meta:
        model = CustomerBillingProfile

    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    customer = factory.SubFactory("monta_customer.factories.customer.CustomerFactory")
    name = factory.Faker("name")


class CustomerContactFactory(factory.django.DjangoModelFactory):
    """
    Customer Contact factory class
    """

    class Meta:
        model = CustomerContact

    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    customer = factory.SubFactory("monta_customer.factories.customer.CustomerFactory")
    contact_name = factory.Faker("name")
    contact_email = factory.Faker("email")
    contact_phone = factory.Faker("phone_number")
    fax_number = factory.Faker("phone_number")
    is_primary = factory.Faker("boolean")
