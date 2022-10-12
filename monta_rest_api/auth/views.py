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

# Rest Framework Imports
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


class CustomAuthTokenView(ObtainAuthToken):
    """
    API endpoint that allows users to be viewed or edited.

    Args:
        ObtainAuthToken (class): ObtainAuthToken class from rest_framework.authtoken.views

    Typical usage example:
        >>> CustomAuthTokenView.as_view()
    """

    def post(self, request, *args, **kwargs) -> Response:
        """
        Post method for CustomAuthToken class

        Args:
            request (Request): Request object from rest_framework.request
            *args (list): List of arguments
            **kwargs (dict): Dictionary of arguments

        Returns:
            Response: Response object from rest_framework.response

        Typical usage example:
            >>> CustomAuthTokenView.as_view().post(request)
        """
        serializer: AuthTokenSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


auth_token_view = CustomAuthTokenView.as_view()


class VerifyAuthTokenView(ObtainAuthToken):
    """
    API endpoint that allows users to be viewed or edited.

    Args:
        ObtainAuthToken (class): ObtainAuthToken class from rest_framework.authtoken.views

    Typical usage example:
        >>> VerifyAuthTokenView.as_view()
    """

    def post(self, request, *args, **kwargs) -> Response:
        """
        Post method for VerifyAuthToken class

        Args:
            request (Request): Request object from rest_framework.request
            *args (list): List of arguments
            **kwargs (dict): Dictionary of arguments

        Returns:
            Response: Response object from rest_framework.response

        Typical usage example:
            >>> VerifyAuthTokenView.as_view().post(request)
        """
        token = request.data["token"]
        try:
            token = Token.objects.get(key=token)
            return Response(
                {"token": token.key, "user_id": token.user_id},
                status=status.HTTP_200_OK,
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


verify_auth_token_view = VerifyAuthTokenView.as_view()


class RefreshAuthTokenView(ObtainAuthToken):
    """
    API endpoint that allows users to be viewed or edited.

    Args:
        ObtainAuthToken (class): ObtainAuthToken class from rest_framework.authtoken.views

    Typical usage example:
        >>> RefreshAuthTokenView.as_view()
    """

    def post(self, request, *args, **kwargs) -> Response:
        """
        Post method for RefreshAuthToken class

        Args:
            request (Request): Request object from rest_framework.request
            *args (list): List of arguments
            **kwargs (dict): Dictionary of arguments

        Returns:
            Response: Response object from rest_framework.response

        Typical usage example:
            >>> RefreshAuthTokenView.as_view().post(request)
        """
        token = request.data["token"]
        try:
            token = Token.objects.get(key=token)
            token.delete()
            token = Token.objects.create(user=token.user)
            return Response(
                {"token": token.key, "user_id": token.user_id},
                status=status.HTTP_200_OK,
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


refresh_auth_token_view = RefreshAuthTokenView.as_view()


class RevokeTokenView(ObtainAuthToken):
    """
    API endpoint that allows users to be viewed or edited.

    Args:
        ObtainAuthToken (class): ObtainAuthToken class from rest_framework.authtoken.views

    Typical usage example:
        >>> RevokeTokenView.as_view()
    """

    def post(self, request, *args, **kwargs) -> Response:
        """
        Post method for RevokeToken class

        Args:
            request (Request): Request object from rest_framework.request
            *args (list): List of arguments
            **kwargs (dict): Dictionary of arguments

        Returns:
            Response: Response object from rest_framework.response

        Typical usage example:
            >>> RevokeTokenView.as_view().post(request)
        """
        token = request.data["token"]
        try:
            token = Token.objects.get(key=token)
            token.delete()
            return Response({"message": "Token revoked"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


revoke_token_view = RevokeTokenView.as_view()
