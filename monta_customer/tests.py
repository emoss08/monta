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
from django.test import TestCase

from monta_customer.factories.customer import (
    DocumentClassificationFactory,
    CustomerFactory,
    CustomerBillingProfileFactory,
)


class DocumentClassificationTest(TestCase):
    def setUp(self):
        self.document_classification = DocumentClassificationFactory.create()

    def test_document_classification_is_created(self):
        """
        Test that the document classification is created
        """
        self.assertTrue(self.document_classification)


class CustomerBillingProfileTest(TestCase):
    def setUp(self):
        self.customer_billing_profile = CustomerBillingProfileFactory.create()

    def test_customer_billing_profile_is_created(self):
        """
        Test that the customer billing profile is created
        """
        self.assertTrue(self.customer_billing_profile)

    def test_customer_billing_profile_has_customer(self):
        """
        Test that the customer billing profile has a customer
        """
        self.assertTrue(self.customer_billing_profile.customer)


class CustomerTest(TestCase):
    def setUp(self):
        self.customer = CustomerFactory.create()

    def test_customer_is_created(self):
        """
        Test that the customer is created
        """
        self.assertTrue(self.customer)

    def test_customer_has_billing_profile(self):
        """
        Test that the customer has a billing profile
        """
        self.assertTrue(self.customer.billing_profiles)

    def test_customer_has_contact(self):
        """
        Test that the customer has a contact
        """
        self.assertTrue(self.customer.contacts)
