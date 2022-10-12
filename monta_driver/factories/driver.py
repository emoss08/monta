# -*- coding: utf-8 -*-
import factory

from monta_driver.models import Driver, DriverProfile


class DriverFactory(factory.django.DjangoModelFactory):
    """
    Driver factory class
    """

    class Meta:
        model = Driver

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )


class DriverProfileFactory(factory.django.DjangoModelFactory):
    """
    Driver profile factory class
    """

    class Meta:
        model = DriverProfile

    driver = factory.SubFactory(DriverFactory)
    address_line_1 = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip_code = factory.Faker("zipcode")
    license_number = factory.Faker("ssn")
    license_state = factory.Faker("state_abbr")
    license_expiration = factory.Faker("date")
    is_hazmat = factory.Faker("boolean")
    is_tanker = factory.Faker("boolean")
    is_double_triple = factory.Faker("boolean")
    is_passenger = factory.Faker("boolean")
