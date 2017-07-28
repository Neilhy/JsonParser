#! /usr/bin/env python
# -*- coding:utf-8 -*-


class JsonError(Exception):
    """Base class for exceptions of json parser"""
    def __init__(self, message, where=None):
        self.where = where
        self.message = message

    def __str__(self):
        if self.where is None:
            return self.message
        else:
            return str(self.where) + " - " + str(self.message)


class JsonEOFError(JsonError):
    """Exception raised for reach eof of file or other input.

    Attributes:
        where -- where the error occurred
        message -- explanation of the error
    """
    pass


class JsonStackError(JsonError):
    """
    Exception raised for json-stack's inside error.

    Attributes:
        where -- where the error occurred
        message -- explanation of the error
    """
    pass


class JsonParseError(JsonError):
    """Exception raised for parsing the json

        Attributes:
            where -- where the error occurred
            message -- explanation of the error
    """
    pass


class JsonFileError(JsonError):
    """Exception raised for parsing the json

        Attributes:
            where -- where the error occurred
            message -- explanation of the error
    """
    pass