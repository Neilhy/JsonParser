#! /usr/bin/env python
# -*- coding:utf -*-


class StackItem(object):
    TYPE_JSON_OBJECT = 0  # {xx:yy}
    TYPE_JSON_OBJECT_BEGIN = 1  # {
    TYPE_JSON_LIST = 2  # [
    TYPE_JSON_OBJECT_KEY = 3  # {xx:}
    TYPE_JSON_VALUE = 4  # bool,string,number,null

    def __init__(self, item_type, item_value):
        self.item_type = item_type
        self.item_value = item_value

    def is_type(self, item_type):
        return self.item_type == item_type

    def get_item_type(self):
        return self.item_type

    def get_item_value(self):
        return self.item_value

    @staticmethod
    def create_json_object(item_value):
        return StackItem(StackItem.TYPE_JSON_OBJECT, item_value)

    @staticmethod
    def create_json_object_key(item_value):
        return StackItem(StackItem.TYPE_JSON_OBJECT_KEY, item_value)

    @staticmethod
    def create_json_object_begin(item_value):
        return StackItem(StackItem.TYPE_JSON_OBJECT_BEGIN, item_value)

    @staticmethod
    def create_json_list(item_value):
        return StackItem(StackItem.TYPE_JSON_LIST, item_value)

    @staticmethod
    def create_json_value(item_value):
        return StackItem(StackItem.TYPE_JSON_VALUE, item_value)
