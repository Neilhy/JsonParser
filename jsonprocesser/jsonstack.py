#! /usr/bin/env python
# -*- coding:utf-8 -*-

import jsonerror


class StackItem(object):
    """
    The stack's item that represent each value and type of json
    """
    TYPE_JSON_OBJECT = 12  # {xx:yy}
    TYPE_JSON_LIST = 13  # [
    TYPE_JSON_OBJECT_KEY = 14  # {xx:}
    TYPE_JSON_VALUE = 15  # bool,string,number,null

    def __init__(self, item_type, item_value):
        self.item_type = item_type
        self.item_value = item_value

    def is_type(self, item_type):
        return self.item_type == item_type

    def get_item_type(self):
        return self.item_type

    def get_item_value(self):
        return self.item_value


class JsonStack(list):
    """
    To store the json data using stack
    """

    def push(self, item):
        super(JsonStack, self).append(item)

    def pop(self, item_type=None):
        if super(JsonStack, self).__len__() == 0:
            raise jsonerror.JsonStackError("The stack is empty.No popping.",
                                           "Popping item")
        item = super(JsonStack, self).pop()
        if item_type is None or item.is_type(item_type):
            return item
        raise jsonerror.JsonStackError("Type is not match.",
                                       "In JsonStack:Popping item.")

    def is_empty(self):
        return super(JsonStack, self).__len__() == 0
