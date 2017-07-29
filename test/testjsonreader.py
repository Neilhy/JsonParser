#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

import jsonprocesser.jsonerror as jsonerror
from jsonprocesser.charreader import CharReader
from jsonprocesser.jsonreader import JsonReader


class JsonReaderTestCase(unittest.TestCase):
    """
    Testing JsonReader
    """

    def test_json_value_string(self):
        json_string = [
            '""',
            '"abc"',
            '" "',
            '"\t"',
            u'"你好\a"',
            '"\u4f60\u597d"',
            '"\u1234"']
        json_string_expected = [
            '', 'abc',
            ' ',
            '\t',
            u'你好\a',
            u'你好', u'\u1234'
        ]
        for i in range(len(json_string)):
            json_reader = JsonReader(CharReader(json_string[i]))
            self.assertEqual(json_reader.json_read(), json_string_expected[i])

    def test_json_value_string_error(self):
        json_string = [
            u'"你好\n "', '"\uu0uu"', 'abc"', '"\r\n\t"'
        ]
        for i in range(len(json_string)):
            json_reader = JsonReader(CharReader(json_string[i]))
            self.assertRaises(jsonerror.JsonParseError, json_reader.json_read)
        json_string2 = [
            '"', '" '
        ]
        for i in range(len(json_string2)):
            json_reader = JsonReader(CharReader(json_string2[i]))
            self.assertRaises(jsonerror.JsonError, json_reader.json_read)

    def test_json_value_bool(self):
        json_bool = [
            'true', 'false', 'true\n \r', 'false\t \r'
        ]
        json_bool_expected = [
            True, False, True, False
        ]
        for i in range(len(json_bool)):
            json_reader = JsonReader(CharReader(json_bool[i]))
            self.assertEqual(json_reader.json_read(), json_bool_expected[i])

    def test_json_value_number(self):
        json_number = [
            '0', '-1', '20', '2e-2', '-2.2E+3', '2.234e-5'
        ]
        json_number_expected = [
            0, -1, 20, 0.02, -2200, 0.00002234
        ]
        for i in range(len(json_number)):
            json_reader = JsonReader(CharReader(json_number[i]))
            self.assertAlmostEqual(
                json_reader.json_read(),
                json_number_expected[i])


if __name__ == '__main__':
    unittest.main()
