# -*- coding: utf-8 -*-
class MethodNotAllowed(Exception):
    """Exception raised when a request method is not allowed."""

    def __init__(self, method):
        self.method = method

    def __str__(self):
        return "Method not allowed: {}".format(self.method)
