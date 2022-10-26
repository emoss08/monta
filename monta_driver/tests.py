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

from monta_driver.factories.driver import DriverFactory, DriverProfileFactory
from monta_driver.forms import AddDriverContactForm, AddDriverForm, AddDriverProfileForm

# Monta Imports
from monta_user.models import Organization


class DriverTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Organization")
        self.driver = DriverFactory.create(organization=self.organization)
        self.driver2 = DriverFactory.create(organization=self.organization)
        self.driver_profile = DriverProfileFactory.create(driver=self.driver)

    def test_driver_form_is_valid(self):
        """
        Test that the driver form is valid
        """
        form = AddDriverForm(
            data={
                "first_name": "Test",
                "last_name": "Driver",
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_form_is_invalid(self):
        """
        Test that the driver form is invalid
        """
        form = AddDriverForm(
            data={
                "first_name": "Test",
            }
        )
        self.assertFalse(form.is_valid())

    def test_driver_profile_form_is_valid(self):
        """
        Test that the driver profile form is valid
        """
        form = AddDriverProfileForm(
            data={
                "driver": self.driver2,
                "address_line_1": "123 Test Street",
                "city": "Test City",
                "state": "NC",
                "zip_code": "12345",
                "license_number": "123456789",
                "license_state": "NC",
                "license_expiration": "2020-01-01",
                "is_hazmat": True,
                "is_tanker": True,
                "is_double_triple": True,
                "is_passenger": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_contact_form_is_valid(self) -> None:
        """
        Test that the driver contact form is valid
        """
        form = AddDriverContactForm(
            data={
                "driver": self.driver,
                "contact_name": "Test Contact",
                "contact_phone": "1234567890",
                "contact_email": "test@test.com",
            }
        )
        self.assertTrue(form.is_valid())

    def test_render_driver_page(self):
        """
        Test that the driver page renders
        """
        response = self.client.get("/driver/")
        self.assertEqual(response.status_code, 302)

    def test_render_driver_edit_page(self):
        """
        Test that the driver edit page renders
        """
        url = "/driver/{}/edit/".format(self.driver.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_render_driver_edit_page_without_driver(self) -> None:
        """
        Test that the driver edit page renders
        """
        url = "/driver/edit/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_driver_search(self) -> None:
        """
        Test that the driver search works
        """
        url = "/driver/search/?q=Test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_driver(self) -> None:
        """
        Test that the driver is deleted
        """
        url = "/driver/{}/delete/".format(self.driver.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
