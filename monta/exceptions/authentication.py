# -*- coding: utf-8 -*-
class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return self.message
