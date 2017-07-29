#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

import json
import jsonparser
import jsonprocesser.jsonerror as jsonerror


class JsonProjectTestCase(unittest.TestCase):
    """
    Testing the project using teacher's data_set
    """

    def setUp(self):
        self.json_ok = [
            ('{}', 1),
            ('{"":""}', 1),
            ('{"a":123}', 1),
            ('{"a":-123}', 1),
            ('{"a":1.23}', 1),
            ('{"a":1e1}', 1),
            ('{"a":true,"b":false}', 1),
            ('{"a":null}', 1),
            ('{"a":[]}', 1),
            ('{"a":{}}', 1),
            (' {"a:": 123}', 1),
            ('{ "a  " : 123}', 1),
            ('{ "a" : 123    	}', 1),
            ('{"true": "null"}', 1),
            ('{"":"\\t\\n"}', 1),
            ('{"\\"":"\\""}', 1),
        ]

        self.json_ok2 = [
            ('{"a":"abcde,:-+{}[]"}', 2),
            ('{"a": [1,2,"abc"]}', 2),
            ('{"d{": "}dd", "a":123}', 2),
            ('{"a": {"a": {"a": 123}}}', 2),
            ('{"a": {"a": {"a": [1,2,[3]]}}}', 2),
            ('{"a": "\\u7f51\\u6613\\b\\r\\n\\t\\f\\/CC\\"\'"}', 3),

            ('{"a":1e-1, "cc": -123.4}', 2),
            ('{ "{ab" : "}123", "\\\\a[": "]\\\\"}', 3),
        ]

        self.json_ex = [
            # exceptions
            ('{"a":[}', 2),
            ('{"a":"}', 2),

            ('{"a":True}', 1),
            ('{"a":Null}', 1),
            ('{"a":foobar}', 2),
            ("{'a':1}", 3),
            ('{1:1}', 2),
            ('{true:1}', 2),
            ('{"a":{}', 2),
            ('{"a":-}', 1),
            ('{"a":[,]}', 2),
            ('{"a":.1}', 1),
            ('{"a":+123}', 1),
            ('{"a":1..1}', 1),
            ('{"a":--1}', 1),
            ('{"a":"""}', 1),
            ('{"a":"\\"}', 1),
        ]
        self.grade = 0
        self.sys_json = json
        self.self_json = jsonparser.JsonParser()

    def test_json_ok(self):
        for json_test in self.json_ok:
            self.self_json.loads(json_test[0])
            string = self.self_json.dumps()
            self.assertEqual(
                self.sys_json.dumps(self.sys_json.loads(json_test[0])),
                string)
            self.grade += 1
        print self.grade

    def test_json_ok2(self):
        for json_test in self.json_ok2:
            self.self_json.loads(json_test[0])
            string = self.self_json.dumps()
            self.assertEqual(
                self.sys_json.dumps(self.sys_json.loads(json_test[0])),
                string)
            self.grade += 1
        print self.grade

    def test_json_ex(self):
        for json_test in self.json_ex:
            jp = jsonparser.JsonParser()
            self.assertRaises(jsonerror.JsonError, jp.loads, json_test[0])
            self.grade += 1
        print self.grade

    def test_json_ok_dict(self):
        for json_test in self.json_ok:
            self.self_json.loads(json_test[0])
            self.assertDictEqual(
                self.sys_json.loads(json_test[0]),
                self.self_json._data)
            self.grade += 1
        print self.grade

    def test_json_ok2_dict(self):
        for json_test in self.json_ok2:
            self.self_json.loads(json_test[0])
            self.assertDictEqual(
                self.sys_json.loads(json_test[0]),
                self.self_json._data)
            self.grade += 1
        print self.grade
