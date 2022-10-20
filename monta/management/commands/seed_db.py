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

# Create tests data for the application

# Core Django Imports
from django.core.management.base import BaseCommand
from django.db import transaction

# Monta Imports
from monta_organization.models import Organization
from monta_user.models import JobTitle
from monta_customer.models import (
    Customer,
    CustomerBillingProfile,
    CustomerContact,
    DocumentClassification
)
from monta_billing.models import ChargeType
from monta_driver.models import Driver, DriverProfile, CommentType
from monta_equipment.models import Equipment, EquipmentType
from monta_locations.models import Location
from monta_order.models import DelayCode, OrderType, RevenueCode, Commodity


class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **options) -> None:
        """Seeds the database with test data"""
        with transaction.atomic():
            self._create_test_data()
        self.stdout.write(self.style.SUCCESS('Successfully seeded test data'))

    @staticmethod
    def _create_test_data() -> None:
        organization = Organization.objects.create(
            name='monta',
            description='test monta organization - do not use in production',
        )
        JobTitle.objects.create(
            name='test',
            description='test job title - do not use in production',
            organization=organization,
        )
        document_classification = DocumentClassification.objects.create(
            name='test',
            description='test document classification - do not use in production',
            organization=organization,
        )
        customer = Customer.objects.create(
            name='test',
            organization=organization,
        )
        billing_profile = CustomerBillingProfile.objects.create(
            name='test',
            is_active=True,
            customer=customer,
            organization=organization,
        )
        billing_profile.document_class.add(document_classification)
        billing_profile.save()
        CustomerContact.objects.create(
            customer=customer,
            organization=organization,
            contact_name='test',
            contact_email='test@test.com',
            is_primary=True,
            is_billing=True,
        )
        ChargeType.objects.create(
            name='test',
            description='test charge type - do not use in production',
            organization=organization,
        )
        driver = Driver.objects.create(
            first_name='test',
            last_name='driver',
            is_active=True,
            organization=organization,
        )
        DriverProfile.objects.create(
            driver=driver,
            organization=organization,
            address_line_1='test',
            address_line_2='test',
            city='test',
            state='NC',
            zip_code='12345',
            license_number='12345',
            license_state='NC',
            license_expiration='2022-01-01',
        )
        CommentType.objects.create(
            name='test',
            description='test comment type - do not use in production',
            organization=organization,
        )
        equipment_type = EquipmentType.objects.create(
            name='test',
            description='test equipment type - do not use in production',
            organization=organization,
        )
        Equipment.objects.create(
            equip_id='test',
            equipment_type=equipment_type,
            organization=organization,
            primary_driver=driver,
            state='NC',
            vin_number='12345',
        )
        Location.objects.create(
            name='test',
            description='test location - do not use in production',
            organization=organization,
            address_line_1='test',
            city='test',
            state='NC',
            zip_code='12345',
        )
        DelayCode.objects.create(
            name='test',
            description='test delay code - do not use in production',
            organization=organization,
        )
        OrderType.objects.create(
            name='test',
            description='test order type - do not use in production',
            organization=organization,
        )
        RevenueCode.objects.create(
            code='test',
            description='test revenue code - do not use in production',
            organization=organization,
        )
        Commodity.objects.create(
            name='test',
            commodity_id='test',
            description='test commodity - do not use in production',
            organization=organization,
        )

    # def _create_output(self) -> None:
    #     # for each create in _create_test_data stdout.write(self.style.SUCCESS('Successfully created {object}'))
    #
    #     if self._create_test_data():
    #         for record in self._create_test_data():
    #             print(record)
    #             self.stdout.write(self.style.SUCCESS(f'Successfully created {record}'))
