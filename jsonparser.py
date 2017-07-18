# -*- coding:utf-8 -*-

from jsonreader import JsonReader
from jsonerror import JsonError
from jsonlog import JsonLog
from stringreader import StringReader
from filereader import FileReader
from charreader import CharReader
from jsonwriter import JsonWriter
from jsondeepcopy import JsonDeepCopy

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
        print self.json_writer.convert(self._data)

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
        self._data = JsonDeepCopy().copy_deep(d)

    def dump_dict(self):
        """
        dump JSON_data to a dict
        """
        return JsonDeepCopy().copy_deep(self._data)

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

# jp.load_file("E:/json.txt")
#
# jp.dump_file('e:/dump_json.txt')

# jp.load_dict({"1": 1, 2: 4})

# print jp.dump_dict() == jp._data, jp.dump_dict() is jp._data

# print jp["a"]
# jp["b"] = "nicai"
# jp["bb"] = "你好"
# print jp["b"],jp["bb"]
# jp[1]=1
