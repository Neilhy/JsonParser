#! /usr/bin/env python
# -*- coding:utf -*-

from eoferror import JsonEOFError


class TokenReader(object):
    """read token one by one from json string"""

    def __init__(self, json_string):
        self.json_string = json_string
        self.json_len = len(json_string)
        self.json_readed = 0

    def read_next_char(self):
        """read next char"""
        self.json_readed += 1
        return self.json_string[self.json_readed]

    def read_not_white_space(self):
        """read next char which is not a white space"""
        while True:
            if self.json_readed == self.json_len:
                raise JsonEOFError("In class : TokenReader",
                                   "EOF of the json_string")
            c = self.json_string[self.json_readed]
            if c not in (' ', '\t', '\n', '\r'):
                return c
            self.read_next_char()  # skip white space

    def read_next_token(self):
        """read next token from json string"""
        pass
