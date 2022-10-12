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
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse


# Third Party Imports
import googlemaps
from asgiref.sync import async_to_sync

# Monta Imports
from monta_locations.models import Location
from monta_organization.models import Integration


@async_to_sync
async def geocode_locations(request: ASGIRequest) -> JsonResponse:
    """
    Process to geocode locations

    Args:
        request (ASGIRequest): The request object.

    Returns:
        JsonResponse: The response object.

    Typical Usage Example:
        >>> from monta_locations.google_api import geocode_locations
        >>> geocode_locations(request)
    """
    # Get the organization's Google API key
    google_api: Integration = await Integration.objects.filter(
        organization=request.user.profile.organization,
        name__exact="google_maps",
        is_active=True,
    ).aget()
    if google_api is None:
        return JsonResponse({"message": "No Google API found."}, status=404)

    gmaps: googlemaps.Client = googlemaps.Client(key=google_api.api_key)

    # Query the database for all locations that need to be geocoded
    locations = Location.objects.filter(
        organization=request.user.profile.organization, is_geocoded=False
    )
    if locations is None:
        return JsonResponse({"message": "No locations found."}, status=404)

    # For each location, geocode it and update the database
    async for location in locations:
        geocode_result = gmaps.geocode(location.get_address_combination)

        if geocode_result:
            location.latitude = geocode_result[0]["geometry"]["location"]["lat"]
            location.longitude = geocode_result[0]["geometry"]["location"]["lng"]
            location.place_id = geocode_result[0]["place_id"]
            location.is_geocoded = True

            # Bulk update the database
            await Location.objects.abulk_update(
                [location],
                fields=["latitude", "longitude", "place_id", "is_geocoded"],
                batch_size=100,
            )
    return JsonResponse({"message": "Locations Geocoded"}, status=200)


# def reverse_geocode_locations(request: ASGIRequest) -> JsonResponse:
#     """ Process to reverse geocode locations """
#     google_api = Integration.objects.filter(organization=request.user.profile.organization).first()
#     gmaps = googlemaps.Client(key=google_api.api_key)
#     locations = Location.objects.filter(organization=request.user.profile.organization)
#     if locations is None:
#         return JsonResponse({"message": "No locations found."}, status=404)
#     for location in locations:
#         reverse_geocode_result = gmaps.reverse_geocode((location.latitude, location.longitude))
#         if reverse_geocode_result:
#             location.address_line_1 = reverse_geocode_result[0]["address_components"][0]["long_name"]
#             location.address_line_2 = reverse_geocode_result[0]["address_components"][1]["long_name"]
#             location.city = reverse_geocode_result[0]["address_components"][2]["long_name"]
#             location.state = reverse_geocode_result[0]["address_components"][4]["long_name"]
#             location.zip_code = reverse_geocode_result[0]["address_components"][6]["long_name"]
#             location.save()
#     return JsonResponse({"message": "Locations Reverse Geocoded"}, status=200)
