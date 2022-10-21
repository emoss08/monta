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

# Core Django Imports
from django.contrib.auth.decorators import login_required
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.db.models import Q

# Third-Party Imports
import googlemaps

# Monta Imports
from monta_locations.models import Location
from monta_organization.models import Integration, OrganizationSettings
from monta_routes import google_api
from monta_routes.models import Route


@login_required
def geocode_locations(request: ASGIRequest) -> JsonResponse:
    """
    Geocode Locations

    :param request: ASGIRequest
    :type request: ASGIRequest
    :return: JsonResponse
    :rtype: JsonResponse
    """
    return google_api.geocode_locations(request)

# NOTE: May add back if requested ability to generate one off routes.
# @login_required
# def get_route_details(
#         request: ASGIRequest,
#         origin: str,
#         destination: str
# ) -> JsonResponse:
#     existing_route = Route.objects.filter(Q(origin__exact=origin) & Q(destination__exact=destination) & Q(
#         organization__exact=request.user.profile.organization))[0]
#     if existing_route:
#         return JsonResponse(
#             {
#                 "result": "success",
#                 "message": "Route already exists.",
#             },
#             status=200
#         )
#     else:
#         integration_api = Integration.objects.filter(
#             organization=request.user.profile.organization,
#             name__exact='google_maps',
#             is_active=True
#         ).first().api_key
#         organization_settings = OrganizationSettings.objects.filter(
#             organization=request.user.profile.organization)[0]
#         gmaps = googlemaps.Client(key=integration_api)
#         first_stop = Location.objects.filter(
#             organization=request.user.profile.organization,
#             location_id__exact=origin
#         ).get().get_address_combination
#         last_stop = Location.objects.filter(
#             organization=request.user.profile.organization,
#             location_id__exact=destination
#         ).get().get_address_combination
#         direction_result = gmaps.distance_matrix(
#             origins=first_stop,
#             destinations=last_stop,
#             mode="driving",
#             departure_time="now",
#             language=organization_settings.language,
#             units=organization_settings.mileage_unit,
#             traffic_model=organization_settings.traffic_model
#         )
#         Route.objects.create(
#             organization=request.user.profile.organization,
#             origin=origin,
#             destination=destination,
#             distance=direction_result['rows'][0]['elements'][0]['distance']['text'].split(' ')[0],
#             duration=direction_result['rows'][0]['elements'][0]['duration']['text'],
#         )
#     return JsonResponse(
#         {
#             "result": "success",
#             "message": "Route created successfully.",
#         },
#         status=200
#     )
