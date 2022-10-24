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

from ajax_datatable import AjaxDatatableView
from braces import views
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.handlers.asgi import ASGIRequest
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_safe
from django.views.decorators.vary import vary_on_cookie

from core.views import MontaCreateView, MontaDeleteView, MontaTemplateView, MontaUpdateView
from monta_billing import forms, models
from monta_customer.models import CustomerBillingProfile, CustomerContact
from monta_driver.forms import SearchForm
from monta_order.models import Order


@method_decorator(require_safe, name="dispatch")
@method_decorator(cache_control(max_age=60 * 60 * 24), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class InteractiveBillingView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, generic.TemplateView
):
    """
    View for Interactive Billing
    """

    template_name = "monta_billing/interactive/index.html"
    permission_required: str = "monta_billing.view_billingqueue"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Get Context Data for Interactive Billing

        :param kwargs: Keyword Arguments
        :type kwargs: Any
        :return: Context Data
        """

        # Queryset for orders ready to be billed out.
        ready_to_bill_orders: QuerySet[models.Order] = (
            Order.objects.filter(
                ready_to_bill=True,
                billed=False,
                status="COMPLETED",
                organization=self.request.user.profile.organization,
            )
            .select_related("customer", "commodity")
            .only(
                "id",
                "order_id",
                "commodity__name",
                "status",
                "customer__customer_id",
                "customer__name",
            )
            .order_by("customer__customer_id")
        )

        context: dict = super().get_context_data(**kwargs)
        context["orders"] = ready_to_bill_orders
        return context


@method_decorator(require_safe, name="dispatch")
@method_decorator(cache_control(max_age=60 * 60 * 24), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class ChargeTypeListView(MontaTemplateView):
    """
    Class to render the Charge Type List View

    Typical Usage Example:
        >>> ChargeTypeListView.as_view()
    """

    template_name = "monta_billing/charge_types/index.html"
    permission_required: str = "monta_billing.view_chargetype"
    context_data: set[str] = {"form": forms.AddChargeTypeForm()}


class ChargeTypeOverviewListView(AjaxDatatableView, mixins.LoginRequiredMixin):
    """
    Class to render the Charge Type overview page.

    Typical Usage Example:
        >>> ChargeTypeOverviewListView.as_view()
    """

    model: Type[models.ChargeType] = models.ChargeType
    title: str = "Charge Type Table"
    initial_order: list[list[str]] = [["name", "desc"]]
    column_defs: list[dict[str, str | bool]] = [
        {
            "name": "name",
            "title": "name",
            "visible": True,
            "orderable": True,
            "searchable": False,
        },
        {
            "name": "description",
            "title": "Description",
            "visible": True,
            "searchable": False,
        },
        {
            "name": "actions",
            "title": "Actions",
            "placeholder": True,
            "visible": True,
            "searchable": False,
            "className": "text-end",
        },
    ]

    def optimize_queryset(self, qs: QuerySet) -> QuerySet[models.ChargeType]:
        """
        Optimize the queryset by prefetching related objects.

        :param qs: Queryset to optimize
        :type qs: QuerySet
        :return: Optimized Queryset
        :rtype: QuerySet
        """
        return qs.order_by("-name")

    def customize_row(self, row: dict[Any, Any], obj: models.ChargeType) -> dict:
        """
        Customize the row by adding the driver information, license number, license state, license expiration, and
        actions.

        :param row: Row to customize
        :type row: dict
        :param obj: Object to customize
        :type obj: models.ChargeType
        :return: Customized Row
        :rtype: dict
        """
        row[
            "actions"
        ] = f"""
        <td class="text-end">
        <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M17.5 11H6.5C4 11 2 9 2 6.5C2 4 4 2 6.5 2H17.5C20 2 22 4 22 6.5C22 9 20 11 17.5 11ZM15 6.5C15 7.9 16.1
        9 17.5 9C18.9 9 20 7.9 20 6.5C20 5.1 18.9 4 17.5 4C16.1 4 15 5.1 15 6.5Z" fill="currentColor"></path>
        <path opacity="0.3" d="M17.5 22H6.5C4 22 2 20 2 17.5C2 15 4 13 6.5 13H17.5C20 13 22 15 22 17.5C22 20 20 22 17.5
        22ZM4 17.5C4 18.9 5.1 20 6.5 20C7.9 20 9 18.9 9 17.5C9 16.1 7.9 15 6.5 15C5.1 15 4 16.1 4 17.5Z"
        fill="currentColor"></path>
        </svg>
        </span>
        </a>
        <a
        data-id="{obj.id}"
        class="btn btn-icon btn-bg-light
        btn-active-color-primary btn-sm me-1 edit-record">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988
        17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355
        21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099
        14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449
        21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z"
        fill="currentColor"></path>
        <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744
        21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799
        20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z"
        fill="currentColor"></path>
        </svg>
        </span>
        </a>
        <a href="{reverse('charge_type_delete', kwargs={'pk': obj.id})}"
        class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm delete-record">
        <span class="svg-icon svg-icon-3">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21
        5 19.6569 5 18V9Z" fill="currentColor"></path>
        <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18
        6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor"></path>
        <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor">
        </path>
        </svg>
        </span>
        </a>
        """
        return row


class ChargeTypeCreateView(MontaCreateView):
    """
    Class to create the Charge Type

    Typical Usage Example:
        >>> ChargeTypeCreateView.as_view()
    """

    permission_required: str = "monta_billing.add_chargetype"
    form_class: Type[forms.AddChargeTypeForm] = forms.AddChargeTypeForm


class ChargeTypeUpdateView(MontaUpdateView):
    """
    Class to update the Charge Type
    """

    permission_required: str = "monta_billing.change_chargetype"
    form_class: Type[forms.AddChargeTypeForm] = forms.AddChargeTypeForm


class ChargeTypeDeleteView(MontaDeleteView):
    """
    Class to delete the Charge Type
    """

    model: Type[models.ChargeType] = models.ChargeType
    permission_required: str = "monta_billing.delete_chargetype"


class ChargeTypeSearchView(
    mixins.LoginRequiredMixin, views.PermissionRequiredMixin, View
):
    """
    Class to delete a driver.
    """

    permission_required: str = "monta_billing.view_chargetypes"

    def get(self, request: ASGIRequest) -> HttpResponse:
        """
        Get request for getting results from the search with params.

        :param request
        :type request: ASGIRequest
        :return HttpResponse of the Charge Type search form
        :rtype HttpResponse
        """
        form: SearchForm = SearchForm()
        query = request.GET["query"] if "query" in request.GET else None
        results: QuerySet[models.ChargeType] | list = []
        if query:
            form: SearchForm = SearchForm({"query": query})
            search_vector: SearchVector = SearchVector(
                "organization__name",
                "name",
                "description",
            )
            search_query: SearchQuery = SearchQuery(query)
            results: QuerySet[models.ChargeType] = (
                models.ChargeType.objects.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(
                    search=search_query, organization=request.user.profile.organization
                )
                .select_related("profile")
                .order_by("-rank")
            )

        return render(
            request,
            "monta_driver/search.html",
            {
                "form": form,
                "query": query,
                "results": results,
            },
        )


class OrderTransferView(mixins.LoginRequiredMixin, views.PermissionRequiredMixin, View):
    """
    Class to list the Transfer Order
    """

    permission_required: str = "monta_billing.transfer_to_billing"

    def post(self, request: ASGIRequest) -> JsonResponse:
        """
        Transfer the order to bill

        :param request
        :type request: ASGIRequest
        :return: JsonResponse
        :rtype: JsonResponse
        """
        orders: QuerySet[Order] = Order.objects.filter(
            organization=request.user.profile.organization,
            ready_to_bill=True,
            billed=False,
            status="COMPLETED",
        )
        for order in orders:
            if order.transferred_to_billing:
                continue
            else:
                models.BillingQueue.objects.create(
                    order=order,
                    organization=request.user.profile.organization,
                )
                order.transferred_to_billing = True
                order.billing_transfer_date = timezone.now()
                order.save()
        return JsonResponse(
            {"result": "success", "message": "Orders transferred to billing queue."},
            status=201,
        )


@login_required
@permission_required("monta_billing.re_bill_orders", raise_exception=True)
def bill_orders(request: ASGIRequest) -> JsonResponse:
    """
    Bill Orders out to customers

    For each order validate that the OrderDocument doucment_class matches the CustomerBillingProfile document_class
    choices. If it does match, bill the order out to customer primary contact email. If it does not match then
    keep the order in the billing queue, and create a billing exception based on the BillingExceptionChoices(PAPERWORK,
    CHARGE, CREDIT, OTHER)

    :param request
    :type request: ASGIRequest
    :return: JsonResponse
    :rtype: JsonResponse
    """
    order_document = []
    billing_requirements = []
    billing_queue: QuerySet[models.BillingQueue] = models.BillingQueue.objects.filter(
        organization=request.user.profile.organization,
    )
    for order in billing_queue:
        customer_billing_profile: QuerySet[
            CustomerBillingProfile
        ] = CustomerBillingProfile.objects.filter(
            customer=order.order.customer,
            organization=request.user.profile.organization,
        )
        customer_contact: CustomerContact = CustomerContact.objects.filter(
            customer=order.order.customer,
            organization=request.user.profile.organization,
            is_billing=True,
        ).first()
        for requirement in customer_billing_profile.values_list(
                "document_class", flat=True
        ):
            billing_requirements.append(requirement)
        for document in order.order.order_documentation.all():
            order_document.append(document.document_class.id)
        if set(billing_requirements).issubset(set(order_document)):
            order.order.billed = True
            order.order.bill_date = timezone.now()
            order.order.save()
            billing_history: models.BillingHistory = (
                models.BillingHistory.objects.create(
                    order=order.order,
                    organization=request.user.profile.organization,
                )
            )
            billing_history.save()
            order.delete()
            send_mail(
                "Invoice for Order: " + order.order.order_id,
                "Please see attached invoice for order: " + order.order.order_id,
                "" + request.user.email,
                [customer_contact.contact_email],
            )
        else:
            missing_requirements: set[Any] = set(billing_requirements) - set(
                order_document
            )
            for requirement in missing_requirements:
                if not models.BillingException.objects.filter(
                        order=order.order,
                        organization=request.user.profile.organization,
                        exception_type="PAPERWORK",
                ):
                    billing_exception: models.BillingException = (
                        models.BillingException.objects.create(
                            order=order.order,
                            organization=request.user.profile.organization,
                            exception_type="PAPERWORK",
                            exception_message="Missing Document " + str(requirement),
                        )
                    )
                    billing_exception.save()
        return JsonResponse(
            {"result": "success", "message": "Orders billed out to customers."},
            status=201,
        )
    return JsonResponse(
        {"result": "success", "message": "No orders to bill."},
        status=201,
    )


@login_required
@permission_required("monta_billing.re_bill_orders", raise_exception=True)
def re_bill_order(request: ASGIRequest, order_id: str) -> JsonResponse:
    """
    Re bill Order.

    :param request
    :type request: ASGIRequest
    :param order_id
    :type order_id: str
    :return: JsonResponse
    :rtype: JsonResponse
    """
    order: Order = Order.objects.filter(
        organization=request.user.profile.organization,
        billed=True,
        order_id=order_id,
    ).get()
    if order:
        models.BillingQueue.objects.create(
            order=order,
            bill_type="CREDIT",
            organization=request.user.profile.organization,
        )
        order.transferred_to_billing = False
        order.billing_transfer_date = None
        order.billed = False
        order.bill_date = None
        order.save()
    return JsonResponse(
        {"result": "success", "message": "Order set back to ready to bill"},
        status=201,
    )
