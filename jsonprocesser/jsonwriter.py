#! /usr/bin/env python
# -*- coding:utf-8 -*-


class JsonWriter(object):
    """
    To convert json_data to json_string
    """
    ESCAPE_DIR_DUMP = {'"': '"', '\\': '\\', '\\/': '/', '\b': 'b', '\f': 'f',
                       '\n': 'n', '\r': 'r', '\t': 't'}

    def convert(self, json_item):
        if isinstance(json_item, dict):
            dict_string = []
            dict_string_begin = '{'
            dict_string_end = '}'
            for dict_item in json_item.items():
                # dict_string_key = '{}{}{}'.format('"', dict_item[0], '"')
                dict_string_key = self.dump_string(dict_item[0])
                dict_string_value = self.convert(dict_item[1])
                dict_string.append(
                    '{}{}{}'.format(dict_string_key, ': ', dict_string_value))
            return dict_string_begin + ', '.join(dict_string) + dict_string_end
        elif isinstance(json_item, list):
            list_string = []
            list_string_begin = '['
            list_string_end = ']'
            for list_item in json_item:
                list_item = self.convert(list_item)
                list_string.append(list_item)
            return list_string_begin + ', '.join(list_string) + list_string_end
        elif isinstance(json_item, bool):
            if json_item:
                json_string = 'true'
            else:
                json_string = 'false'
            return json_string
        elif json_item is None:
            return 'null'
        elif isinstance(json_item, unicode):  # .decode('string_escape')
            # return '"' + json_item.encode('unicode-escape') + '"'
            # return '"' + json_item.encode('unicode-escape') + '"'
            return self.dump_string(json_item)
        elif isinstance(json_item, str):
            return '{}{}{}'.format('"', json_item, '"')
        else:
            return str(json_item)
            # return unicode(json_item)

    def dump_string(self, s):
        s = s.encode('unicode-escape').decode('string_escape')
        new_s = '"'
        for i in range(0, len(s)):
            if (i + 1) < len(s) and s[i:i + 2] == '\u':
                new_s += s[i]
            elif s[i] in JsonWriter.ESCAPE_DIR_DUMP:
                new_s += '\\'
                new_s += JsonWriter.ESCAPE_DIR_DUMP[s[i]]
            else:
                new_s += s[i]
        new_s += '"'
        return new_s
