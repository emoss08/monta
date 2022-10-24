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


class MontaCoreException(Exception):
    """
    Base class for all exceptions to be raised by Monta.
    """

    def __init__(self, message: str, status_code: int) -> None:
        """
        This is the constructor for the AuthenticationError class.

        :param message: The error message
        :type message: str
        :param status_code: The status code
        :type status_code: int
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)

    def __str__(self) -> str:
        """
        This is the string representation of the AuthenticationError class.

        :return: The error message
        :rtype: str
        """
        return f"{self.message} (Status Code: {self.status_code})"


class ApplicationError(MontaCoreException):
    """
    Base class for all application errors.
    """
    pass


class AuthenticationError(MontaCoreException):
    """
    This is the error class for the monta_authentication app.
    """

    def __init__(self):
        """
        This is the constructor for the AuthenticationError class.
        """
        super().__init__("Authentication failed.", 401)


class UserNotFound(MontaCoreException):
    """
    Exception to raise when a user is not found.
    """

    def __init__(self):
        """
        This is the constructor for the UserNotFound class.
        """
        super().__init__("User not found.", 404)


class UserAlreadyExists(MontaCoreException):
    """
    Exception to raise when a user already exists.
    """

    def __init__(self):
        """
        This is the constructor for the UserAlreadyExists class.
        """
        super().__init__("User already exists.", 409)


class UserIsLastAdmin(MontaCoreException):
    """
    Exception to raise if the user is the last admin.
    """

    def __init__(self):
        """
        This is the constructor for the UserIsLastAdmin class.
        """
        super().__init__("User is the last admin.", 403)
