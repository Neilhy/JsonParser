#! /usr/bin/env python
# -*- coding:utf -*-
from jsonerror import JsonError


class JsonEOFError(JsonError):
    """Exception raised for reach eof of file or other input.

    Attributes:
        where -- where the error occurred
        message -- explanation of the error
    """

    def __init__(self, where, message):
        self.where = where
        self.message = message
