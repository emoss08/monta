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

from typing import Any, Type

from core.views import (
    MontaCreateView,
    MontaDeleteView,
    MontaTemplateView,
    MontaUpdateView,
)
from monta_customer import forms, models


class CustomerListView(MontaTemplateView):
    """
    CustomerListView is a view that renders a template.
    """

    template_name = "monta_customer/index.html"
    permission_required = "monta_customer.view_customer"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Get the context data for the view.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["customers"] = models.Customer.objects.filter(
            organization=self.request.user.profile.organization
        )
        return context


class CustomerCreateView(MontaCreateView):
    """
    View for creating a customer
    """

    model: Type[models.Customer] = models.Customer
    form_class: Type[forms.AddCustomerForm] = forms.AddCustomerForm
    permission_required = "monta_customer.create_customer"


class CustomerUpdateView(MontaUpdateView):
    model: Type[models.Customer] = models.Customer
    form_class: Type[forms.AddCustomerForm] = forms.AddCustomerForm
    permission_required = "monta_customer.update_customer"


class CustomerDeleteView(MontaDeleteView):
    model: Type[models.Customer] = models.Customer
