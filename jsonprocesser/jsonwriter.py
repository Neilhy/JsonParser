#! /usr/bin/env python
# -*- coding:utf-8 -*-


class JsonWriter(object):
    """
    To convert json_data to json_string
    """
    def convert(self, json_item):
        if isinstance(json_item, dict):
            dict_string = []
            dict_string_begin = '{'
            dict_string_end = '}'
            for dict_item in json_item.items():
                dict_string_key = '"' + dict_item[0] + '"'
                dict_string_value = self.convert(dict_item[1])
                dict_string.append(dict_string_key + ':' + dict_string_value)
            return dict_string_begin + ','.join(dict_string) + dict_string_end
        elif isinstance(json_item, list):
            list_string = []
            list_string_begin = '['
            list_string_end = ']'
            for list_item in json_item:
                list_item = self.convert(list_item)
                list_string.append(list_item)
            return list_string_begin + ','.join(list_string) + list_string_end
        elif isinstance(json_item, bool):
            if json_item:
                json_string = 'true'
            else:
                json_string = 'false'
            return json_string
        elif json_item is None:
            return 'null'
        elif isinstance(json_item, unicode):  # include unicode
            return '"' + json_item.encode('unicode-escape') + '"'
        elif isinstance(json_item, str):
            return '"' + json_item + '"'
        else:
            return str(json_item)
