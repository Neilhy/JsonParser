# -*- coding:utf-8 -*-

from jsonreader import JsonReader
from jsonerror import JsonError
from jsonlog import JsonLog
from stringreader import StringReader
from filereader import FileReader
from charreader import CharReader

log = JsonLog(__name__)


class JsonParser(object):
    """Parse json using Python"""

    def __init__(self):
        self._data = {}
        self.json_reader = None

    def loads(self, s):
        """load JSON from string"""
        char_reader = CharReader(StringReader(s))
        self.json_reader = JsonReader(char_reader)
        try:
            self._data = self.json_reader.json_read()
        except JsonError as json_error:
            # log.exception(msg=json_error.message)
            print json_error
        # print self._data[0].get_item_value(), self._data[1].get_item_value()
        print self._data


jp = JsonParser()
# jp.loads(
#     '{"a":1}'
# )
#  {'City': 'SAN FRANCISCO', 'Zip': '94107', 'Country': 'US', 'precision': 'zip', 'Longitude': -122.3959, 'State': 'CA', 'Address': '', 'Latitude': 37.7668} {'City': 'SUNNYVALE', 'Zip': '94085', 'Country': 'US', 'precision': 'zip', 'Longitude': -122.02602, 'State': 'CA', 'Address': '', 'Latitude': 37.371991}
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
jp.loads(
    """
    {
"a":1,
"b":[1,2,3],
"c":{"c1":1},
"d":[1,2,3,{"d1":1}],
"e":[1,2,3,[4,5,6]],
"f":{"f1":1,"f2":[1,2,3],"f3":{"f4":1}},
"u":"\u6ff3",
"a":4
}

    """
)
