#! /usr/bin/env python
# -*- coding:utf-8 -*-


class JsonWriter(object):
    """
    To convert json_data to json_string
    """

    def convert(self, json_item):
        if isinstance(json_item, dict):
            dict_string = []
            dict_string_begin = u'{'
            dict_string_end = u'}'
            for dict_item in json_item.items():
                dict_string_key = u'{}{}{}'.format('"', unicode(dict_item[0]),
                                                   '"')
                dict_string_value = self.convert(dict_item[1])
                # dict_string.append(dict_string_key + u':' + unicode(dict_string_value))
                dict_string.append(u'{}{}{}'.format(dict_string_key, u':',
                                                    unicode(dict_string_value)))
            return unicode(
                dict_string_begin + u','.join(dict_string) + dict_string_end)
        elif isinstance(json_item, list):
            list_string = []
            list_string_begin = u'['
            list_string_end = u']'
            for list_item in json_item:
                list_item = self.convert(list_item)
                list_string.append(list_item)
            return unicode(
                list_string_begin + u','.join(list_string) + list_string_end)
        elif isinstance(json_item, bool):
            if json_item:
                json_string = u'true'
            else:
                json_string = u'false'
            return json_string
        elif json_item is None:
            return u'null'
        elif isinstance(json_item, unicode):  # include unicode
            return u'"' + json_item.encode('unicode-escape') + u'"'
        elif isinstance(json_item, str):
            return u'{}{}{}'.format(u'"', unicode(json_item), u'"')
        else:
            # return str(json_item)
            return unicode(json_item)
