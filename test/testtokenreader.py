#! /usr/bin/env python
# -*- coding:utf-8 -*-
import unittest

import jsonprocesser.jsonerror
from jsonprocesser.charreader import CharReader

from jsonprocesser.tokenreader import TokenReader
from jsonprocesser.tokenreader import TokenType


class TokenReaderTestCase(unittest.TestCase):
    """
    Testing TokenReader
    """

    def test_next_token(self):
        json_string = ["{", '}', ":", ',', '[', ']', '1']
        token_type_expect = [
            TokenType.START_OBJ,
            TokenType.END_OBJ,
            TokenType.COLON,
            TokenType.COMMA,
            TokenType.START_LIST,
            TokenType.END_LIST,
            TokenType.NUMBER
        ]
        token_reader = TokenReader(CharReader(json_string))
        for i in range(len(token_type_expect)):
            token_type = token_reader.read_next_token()
            self.assertEqual(token_type, token_type_expect[i],
                             "TokenType not equal.")

    def test_read_string(self):
        json_string = '"testing  "'
        expected_string = "testing  "
        token_reader = TokenReader(CharReader(json_string))
        self.assertEqual(token_reader.read_string(), expected_string)

    def test_read_bool(self):
        json_string = "true"
        expected_string = True
        token_reader = TokenReader(CharReader(json_string))
        self.assertEqual(token_reader.read_bool(), expected_string)

    def test_read_null(self):
        json_string = "null"
        expected_string = None
        token_reader = TokenReader(CharReader(json_string))
        self.assertEqual(token_reader.read_null(), expected_string)

    def test_read_number(self):
        json_string = [
            "1", "1e+10", "9e-10", "-2e+4", "-4e-6", "1.234", "12.34E+3",
            "-123.0E-2"
        ]
        expected_string = [
            1, 10000000000, 9e-10, -20000, -0.000004, 1.234, 12340, -1.23
        ]
        for i in range(len(json_string)):
            token_reader = TokenReader(CharReader(json_string[i]))
            self.assertEqual(token_reader.read_number(), expected_string[i])

    def test_string_to_int(self):
        chars = list("123456789")
        expect_int = 123456789
        self.assertEqual(TokenReader.string_to_int(chars), expect_int)

        chars2 = list("12345678901234567890")
        self.assertRaises(jsonerror.JsonParseError, TokenReader.string_to_int,
                          chars2)

        chars3 = list("9223372036854775808")
        self.assertRaises(jsonerror.JsonParseError, TokenReader.string_to_int,
                          chars3)

    def test_string_to_fraction(self):
        chars = list("123456789")
        expect_int = 0.123456789
        self.assertAlmostEqual(TokenReader.string_to_fraction(chars), expect_int)

        chars2 = list("12345678901234567")
        self.assertRaises(jsonerror.JsonParseError, TokenReader.string_to_fraction,
                          chars2)


if __name__ == '__main__':
    # unittest.TestLoader().loadTestsFromName(
    #     "test.TokenReaderTestCase.test_read_string")
    unittest.main()
