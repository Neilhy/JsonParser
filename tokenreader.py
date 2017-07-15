#! /usr/bin/env python
# -*- coding:utf -*-

from eoferror import JsonEOFError
from parseerror import ParseError
from jsonlog import JsonLog
from token import TokenType

import sys

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
        elif c in ('t', 'f'):
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

    def read_boolean(self):
        ch = self.json_string[self.json_readed]
        if ch == 't':
            expected = 'rue'
        elif ch == 'f':
            expected = 'alse'
        else:
            raise ParseError(
                message="Unexpected char:" + ch,
                where="In class : TokenReader\nIn method : read_string")
        for i in range(len(expected)):
            ech = self.read_next_char()
            if ech != expected[i]:
                raise ParseError(
                    message="Unexpected char:" + ech,
                    where="In class : TokenReader\nIn method : read_string")
        return ch == 't'

    def read_null(self):
        expected = 'null'
        for i in range(len(expected)):
            ech = self.read_next_char()
            if ech != expected[i]:
                raise ParseError(
                    message="Unexpected char:" + ech,
                    where="In class : TokenReader\nIn method : read_string")

    def read_number(self):
        """
        number
            int
            int frac
            int exp
            int frac exp
        int
            digit
            digit1-9 digits
            - digit
            - digit1-9 digits
        frac
            . digits
        exp
            e digits
        digits
            digit
            digit digits
        """
        int_part = []  # ###.xxxExxx
        fra_part = []  # xxx.###Exxx
        exp_part = []  # xxx.xxxE###

        INT_PART = 0
        FRA_PART = 1
        EXP_PART = 2
        NUMBER_END = 3

        has_fra_part = False
        has_exp_part = False

        ch = self.json_string[self.json_readed]
        minus_sign = (ch == '-')
        exp_minus_sign = False
        if minus_sign:
            self.read_next_char()

        status = INT_PART
        while True:
            if self.json_readed == self.json_len:
                status = NUMBER_END
            else:
                ch = self.json_string[self.json_readed]

            if status == INT_PART:
                if '0' <= ch <= '9':
                    int_part.append(ch)
                    self.read_next_char()

                elif ch == '.':
                    if not int_part:
                        raise ParseError(
                            message="Expected int_part : ###.xxxExxx but None",
                            where="In class : TokenReader\nIn method : read_number_INT_PART_.")
                    self.read_next_char()
                    has_fra_part = True
                    status = FRA_PART

                elif ch in ('e', 'E'):
                    if not int_part:
                        raise ParseError(
                            message="Expected int_part : ###.xxxExxx but None",
                            where="In class : TokenReader\nIn method : read_number_INT_PART_e")
                    self.read_next_char()
                    has_exp_part = True
                    sign_char = self.json_string[self.json_readed]
                    if (sign_char not in ('-', '+')) and (
                            not isinstance(sign_char, int)):
                        raise ParseError(
                            message="Expected '-' or '+' or digit but is " + sign_char,
                            where="In class : TokenReader\nIn method : read_number_INT_PART_e")
                    elif sign_char in ('-', '+'):
                        exp_minus_sign = (sign_char == '-')
                        self.read_next_char()
                    status = EXP_PART

                else:
                    if not int_part:
                        raise ParseError(
                            message="Unexpected char:" + ch,
                            where="In class : TokenReader\nIn method : read_number_INT_PART_")
                    status = NUMBER_END

            elif status == FRA_PART:
                if '0' <= ch <= '9':
                    fra_part.append(ch)
                    self.read_next_char()

                elif ch in ('e', 'E'):
                    if not int_part:
                        raise ParseError(
                            message="Expected int_part : ###.xxxExxx but None",
                            where="In class : TokenReader\nIn method : read_number_FRA_PART_e")
                    self.read_next_char()
                    has_exp_part = True
                    sign_char = self.json_string[self.json_readed]
                    if (sign_char not in ('-', '+')) and (
                            not isinstance(sign_char, int)):
                        raise ParseError(
                            message="Expected '-' or '+' or digit but is " + sign_char,
                            where="In class : TokenReader\nIn method : read_number_FRA_PART_e")
                    elif sign_char in ('-', '+'):
                        exp_minus_sign = (sign_char == '-')
                        self.read_next_char()
                    status = EXP_PART

                else:
                    if not fra_part:
                        raise ParseError(
                            message="Unexpected char:" + ch,
                            where="In class : TokenReader\nIn method : read_number_FRA_PART_")
                    status = NUMBER_END

            elif status == EXP_PART:
                if '0' <= ch <= '9':
                    exp_part.append(ch)
                    self.read_next_char()
                else:
                    if not exp_part:
                        raise ParseError(
                            message="Unexpected char:" + ch,
                            where="In class : TokenReader\nIn method : read_number_EXP_PART_"
                        )
                    status = NUMBER_END

            elif status == NUMBER_END:  # Start to convert string to number
                if not int_part:
                    raise ParseError(
                        message="Expected int_part : ###.xxxExxx but None",
                        where="In class : TokenReader\nIn method : read_number_END"
                    )
                if minus_sign:
                    int_value = - self.string_to_int(int_part)
                else:
                    int_value = self.string_to_int(int_part)

                if not has_fra_part and not has_exp_part:
                    return int_value
                if has_fra_part and not fra_part:
                    raise ParseError("Expected fra_part : xxx.###Exxx but None",
                                     "In class : TokenReader\nIn method : read_number_END")
                if has_fra_part:
                    if minus_sign:
                        fra_value = -self.string_to_fraction(fra_part)
                    else:
                        fra_value = self.string_to_fraction(fra_part)
                else:
                    fra_value = 0.0

                if has_exp_part and not exp_part:
                    raise ParseError("Expected exp_part : xxx.xxxE### but None",
                                     "In class : TokenReader\nIn method : read_number_END")
                if has_exp_part:
                    if exp_minus_sign:
                        number = (int_value + fra_value) * pow(
                            10, -self.string_to_int(exp_part))
                    else:
                        number = (int_value + fra_value) * pow(
                            10, self.string_to_int(exp_part))

                    if minus_sign and number > 0:  # eg: -2.2E2 < 0
                        number = -number
                else:
                    number = int_value + fra_value

                if not sys.float_info.min <= number <= sys.float_info.max:
                    raise ParseError(
                        "Number is too large or small : " + str(number),
                        "In class : TokenReader\nIn method : read_number_END"
                    )
                return number

    @staticmethod
    def string_to_int(chars):
        if len(chars) > 19:  # 9223372036854775807L
            raise ParseError("Number string is too long : " + str(chars),
                             "string_to_int")
        n = 0
        for i in range(len(chars)):
            n = n * 10 + int(chars[i])
            if n > sys.maxsize:
                raise ParseError("Number is too large : " + str(chars),
                                 "string_to_int")
        return n

    @staticmethod
    def string_to_fraction(chars):
        if len(chars) > 16:  # max=1.7976931348623157e+308
            raise ParseError("Number string is too long : " + str(chars),
                             "string_to_int")
        d = 0.0
        for i in range(len(chars)):
            n = int(chars[i])
            d += 0 if n == 0 else n / pow(10, i + 1)
        return d
