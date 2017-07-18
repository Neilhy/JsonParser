#! /usr/bin/env python
# -*- coding:utf -*-


class StackItem(object):
    """
    The stack's item that represent each value and type of json
    """
    TYPE_JSON_OBJECT = 0  # {xx:yy}
    TYPE_JSON_LIST = 1  # [
    TYPE_JSON_OBJECT_KEY = 2  # {xx:}
    TYPE_JSON_VALUE = 3  # bool,string,number,null

    def __init__(self, item_type, item_value):
        self.item_type = item_type
        self.item_value = item_value

    def is_type(self, item_type):
        return self.item_type == item_type

    def get_item_type(self):
        return self.item_type

    def get_item_value(self):
        return self.item_value
