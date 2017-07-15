#! /usr/bin/env python
# -*- coding:utf -*-

from eoferror import JsonEOFError
from parseerror import ParseError
from jsonlog import JsonLog
from token import TokenType

log = JsonLog(__name__)


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
                raise JsonEOFError(where="In class : TokenReader",
                                   message="EOF of the json_string")
            c = self.json_string[self.json_readed]
            if c not in (' ', '\t', '\n', '\r'):
                return c
            self.read_next_char()  # skip white space

    def read_next_token(self):
        """read next token from json string"""
        c = '???'
        try:
            c = self.read_not_white_space()
        except JsonEOFError as eof_error:
            log.warning(str(eof_error), exc_info=True)
            return TokenType.END_DOC

        if c == '{':
            self.read_next_char()
            return TokenType.START_OBJ
        elif c == '}':
            self.read_next_char()
            return TokenType.END_OBJ
        elif c == '[':
            self.read_next_char()
            return TokenType.START_ARRAY
        elif c == ']':
            self.read_next_char()
            return TokenType.END_ARRAY
        elif c == ':':
            self.read_next_char()
            return TokenType.COLON
        elif c == ',':
            self.read_next_char()
            return TokenType.COMMA
        elif c == '\"':
            return TokenType.STRING
        elif c == 'n':
            return TokenType.NULL
        elif c == 't' or c == 'f':
            return TokenType.BOOLEAN
        elif c == '-' or ('0' <= c <= '9'):
            return TokenType.NUMBER
        else:
            # parse_error = ParseError(
            #     message="Parse error when try to get next token.",
            #     where="In class : TokenReader\nIn method : read_next_token")
            # log.exception(str(parse_error))
            raise ParseError(
                message="Parse error when try to get next token.",
                where="In class : TokenReader\nIn method : read_next_token")

    def read_string(self):
        string = []
        # first char must be "
        ch = self.json_string[self.json_readed]
        if ch != '\"':
            raise ParseError(
                message="Expected \" but actual is: " + ch,
                where="In class : TokenReader\nIn method : read_string")
        while True:
            ch = self.read_next_char()
            if ch == '\\':  # escape: \" \\ \/ \b \f \n \r \t
                ech = self.read_next_char()

                if ech == "\"":
                    string.append("\"")
                elif ech == "\\":
                    string.append("\\")
                elif ech == "/":
                    string.append("/")
                elif ech == "b":
                    string.append("b")
                elif ech == "f":
                    string.append("f")
                elif ech == "n":
                    string.append("n")
                elif ech == "r":
                    string.append("r")
                elif ech == "t":
                    string.append("t")
                elif ech == "u":  # read an unicode uXXXX
                    u = 0
                    for i in range(4):
                        uch = self.read_next_char()
                        if '0' <= uch <= '9':
                            u = (u << 4) + int(uch)
                        elif 'a' <= uch <= 'f':
                            u = (u << 4) + int(uch, 16)
                        elif 'A' <= uch <= "F":
                            u = (u << 4) + int(uch, 16)
                        else:
                            raise ParseError(
                                message="Unexpected char:" + uch,
                                where="In class : TokenReader\nIn method : read_string")
                    string.append(chr(u))
                else:
                    raise ParseError(
                        message="Unexpected char:" + ech,
                        where="In class : TokenReader\nIn method : read_string")

            elif ch == '\"':  # end of string
                break
            elif ch == '\r' or ch == '\n':
                raise ParseError(
                    message="Unexpected char:" + ch,
                    where="In class : TokenReader\nIn method : read_string")
            else:
                string.append(ch)
        return ''.join(string)
