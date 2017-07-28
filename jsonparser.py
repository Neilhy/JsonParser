#! /usr/bin/env python
# -*- coding:utf-8 -*-

import logging

import jsonprocesser.jsonerror as jsonerror
from jsonprocesser.charreader import CharReader
from jsonprocesser.jsondeepcopy import JsonDeepCopy
from jsonprocesser.jsonwriter import JsonWriter

from jsonprocesser.jsonreader import JsonReader


class JsonParser(object):
    """Parse json using Python"""

    def __init__(self):
        self._data = {}
        self.json_reader = None
        self.json_writer = None

    def loads(self, s):
        """
        load JSON from string

        Attributes:
        s -- JSON string
        """
        char_reader = CharReader(s)
        self.json_reader = JsonReader(char_reader)
        try:
            self._data = self.json_reader.json_read()
        except jsonerror.JsonError as json_error:
            logging.exception(msg=json_error.message)
            raise json_error


        return self._data

    def load_file(self, f):
        """
        load JSON from file

        Attributes:
        f -- file_path
        """
        with open(f, 'r') as json_file:
            json_string = json_file.read()
        if json_string is None:
            raise jsonerror.JsonFileError(
                'Open json file error.',
                'In JsonParser:load_file.'
            )
        char_reader = CharReader(json_string)
        self.json_reader = JsonReader(char_reader)
        try:
            self._data = self.json_reader.json_read()
        except jsonerror.JsonError as json_error:
            logging.exception(msg=json_error.message)
            raise json_error
        print self._data

    def dumps(self):
        """
        dumps JSON to string

        """
        self.json_writer = JsonWriter()
        return unicode(self.json_writer.convert(self._data))

    def dump_file(self, f):
        """
        dump JSON to file

        Attributes:
        f -- file_path
        """
        with open(f, 'w') as json_file:
            json_file.write(self.dumps())

    def load_dict(self, d):
        """
        load JSON_data from d

        Attributes:
        d -- dict
        """
        if isinstance(d, dict):
            self._data = JsonDeepCopy().copy_deep(d)
        else:
            raise ValueError("d is not a dict.")

    def dump_dict(self):
        """
        dump JSON_data to a dict
        """
        return JsonDeepCopy().copy_deep(self._data)

    def update(self, d):
        """
        update the _data by d
        :param d: new dict
        """
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(k, str):
                    self._data[k] = v
        else:
            raise ValueError("d is not a dict.")

    def __getitem__(self, item):
        """
        Get item by []
        :param item: key of dict
        :return: value of dict
        """
        JsonParser.check_key(item)
        return self._data[item]

    def __setitem__(self, key, value):
        """
        Set key,value in dict
        :param key: key of dict
        :param value: new value of dict
        """
        JsonParser.check_key(key)
        self._data[key] = value

    @staticmethod
    def check_key(key):
        if not isinstance(key, str):
            raise TypeError("Key must be str type.")


if __name__ == '__main__':
    """
        示例代码
    """
    jp = JsonParser()
    jp.loads(
        """
        [
          {
             "precision": "zip",
             "Latitude":  37.7668,
             "Longitude": -122.3959,
             "Address":   "",
             "City":      "SAN FRANCISCO",
             "State":     "CA",
             "Zip":       "94107",
             "Country":   "US"
          },
          {
             "precision": "zip",
             "Latitude":  37.371991,
             "Longitude": -122.026020,
             "Address":   "",
             "City":      "SUNNYVALE",
             "State":     "CA",
             "Zip":       "94085",
             "Country":   "US"
          }
       ]
    
        """
    )
    print jp.dumps()

    jp.loads(
        """
        {
    "a":"你好",
    "b":[1,"吗",3],
    "c":{"c1":1},
    "d":[1,2,3,{"嘛1":1}],
    "e":[1,2,3,[4,5,6]],
    "f":{"f1":1,"f2":[1,2,3],"f3":{"f4":1}},
    "u":"\u6ff3"
    }

    """
    )
    print jp.dumps()

    # jp.load_file("E:/json.txt")
    # jp.dump_file('e:/dump_json.txt')

    # jp.load_dict({"1": 1, 2: 4})

    # print jp.dump_dict() == jp._data, jp.dump_dict() is jp._data
