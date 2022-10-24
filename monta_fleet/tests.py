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

from django.test import TestCase

from monta_fleet.factories.fleet import FleetFactory
from monta_fleet.forms import AddFleetForm


class TestMontaFleet(TestCase):
    def setUp(self) -> None:
        self.fleet = FleetFactory.create()

    def test_fleet_is_created(self) -> None:
        """
        Test that the fleet is created
        """
        self.assertTrue(self.fleet)

    def test_render_fleet_page(self) -> None:
        """
        Test that the driver page renders
        """
        response = self.client.get("/fleet/")
        self.assertEqual(response.status_code, 302)

    def test_render_fleet_edit_page(self) -> None:
        response = self.client.get("/fleet/{}/edit/".format(self.fleet.id))
        self.assertEqual(response.status_code, 302)


class TestMontaFleetForms(TestCase):
    def setUp(self) -> None:
        self.fleet = FleetFactory.create()

    def test_fleet_form_is_valid(self) -> None:
        """
        Test that the fleet form is valid
        """
        form: AddFleetForm = AddFleetForm(
            data={
                "organization": self.fleet.organization,
                "name": "Test Fleet",
                "fleet_id": "123",
                "description": "Test Description",
                "fleet_manager": self.fleet.fleet_manager,
                "is_active": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_fleet_form_is_invalid(self) -> None:
        """
        Test that the fleet form is invalid
        """
        form: AddFleetForm = AddFleetForm(
            data={
                "name": "Test Fleet",
                "fleet_id": "123",
                "description": "Test Description",
            }
        )
        self.assertFalse(form.is_valid())
