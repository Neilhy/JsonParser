#! /usr/bin/env python
# -*- coding:utf-8 -*-
from jsonerror import JsonError


class JsonEOFError(JsonError):
    """Exception raised for reach eof of file or other input.

    Attributes:
        where -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, where=None):
        self.where = where
        self.message = message

    def __str__(self):
        if self.where is None:
            return self.message
        else:
            return str(self.where) + " - " + str(self.message)
