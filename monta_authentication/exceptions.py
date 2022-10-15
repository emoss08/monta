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


class AuthenticationError(Exception):
    """
    This is the error class for the monta_authentication app.
    """

    def __init__(self, message: str = "Authentication Error", status_code: int = 400):
        """
        This is the constructor for the AuthenticationError class.

        :param message: The error message
        :type message: str
        :param status_code: The status code
        :type status_code: int
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        This is the string representation of the AuthenticationError class.

        :return: The error message
        :rtype: str
        """
        return f"{self.message} (Status Code: {self.status_code})"
