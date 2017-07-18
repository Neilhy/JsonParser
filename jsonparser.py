# -*- coding:utf-8 -*-

from jsonreader import JsonReader
from jsonerror import JsonError
from jsonlog import JsonLog
from stringreader import StringReader
from filereader import FileReader
from charreader import CharReader
from jsonwriter import JsonWriter

log = JsonLog(__name__)


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
        char_reader = CharReader(StringReader(s))
        self.json_reader = JsonReader(char_reader)
        try:
            self._data = self.json_reader.json_read()
        except JsonError as json_error:
            # log.exception(msg=json_error.message)
            print json_error
        print self._data

    def load_file(self, f):
        """
        load JSON from file

        Attributes:
        f -- file_path
        """
        char_reader = CharReader(FileReader(f))
        self.json_reader = JsonReader(char_reader)
        try:
            self._data = self.json_reader.json_read()
        except JsonError as json_error:
            # log.exception(msg=json_error.message)
            print json_error
        print self._data

    def dumps(self):
        """
        dumps JSON to string

        """
        self.json_writer = JsonWriter()
        return self.json_writer.convert(self._data)

    def dump_file(self, f):
        """
        dump JSON to file

        Attributes:
        f -- file_path
        """
        with open(f, 'w') as json_file:
            json_file.write(self.dumps())


jp = JsonParser()
# jp.loads(
#     '{"a":1}'
# )
#  {'City': 'SAN FRANCISCO', 'Zip': '94107', 'Country': 'US', 'precision': 'zip', 'Longitude': -122.3959, 'State': 'CA', 'Address': '', 'Latitude': 37.7668} {'City': 'SUNNYVALE', 'Zip': '94085', 'Country': 'US', 'precision': 'zip', 'Longitude': -122.02602, 'State': 'CA', 'Address': '', 'Latitude': 37.371991}
# jp.loads(
#     """
#     [
#       {
#          "precision": "zip",
#          "Latitude":  37.7668,
#          "Longitude": -122.3959,
#          "Address":   "",
#          "City":      "SAN FRANCISCO",
#          "State":     "CA",
#          "Zip":       "94107",
#          "Country":   "US"
#       },
#       {
#          "precision": "zip",
#          "Latitude":  37.371991,
#          "Longitude": -122.026020,
#          "Address":   "",
#          "City":      "SUNNYVALE",
#          "State":     "CA",
#          "Zip":       "94085",
#          "Country":   "US"
#       }
#    ]
#
#     """
# )
# jp.loads(
#     """
#     {
# "a":1,
# "b":[1,2,3],
# "c":{"c1":1},
# "d":[1,2,3,{"d1":1}],
# "e":[1,2,3,[4,5,6]],
# "f":{"f1":1,"f2":[1,2,3],"f3":{"f4":1}},
# "u":"\u6ff3"
# }
#
#     """
# )
# jp.loads(
#     """
#     true
#     """
# )

# jp.loads(
#     """
#     false
#     """
# )
# jp.loads(
#     """{
#     "a":10e-10
#     }
#     """
# )
# jp.loads(
#     """{
#     "b":-1e+10
#     }
#     """
# )
# jp.dumps()
#
# jp.loads(
#     """"b"
#     """
# )
# jp.dumps()
#
# jp.loads(
#     """10
#     """
# )
# jp.dumps()

# jp.loads(
#     """null
#     """
# )
# jp.loads(
#     """{
#     "b":null
#     }
#     """
# )

jp.load_file("E:/json.txt")
#
jp.dump_file('e:/dump_json.txt')

