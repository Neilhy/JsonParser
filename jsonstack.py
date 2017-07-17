#! /usr/bin/env python
# -*- coding:utf -*-

from jsonstackerror import JsonStackError


class JsonStack(list):
    def push(self, item):
        super(JsonStack, self).append(item)

    def pop(self, item_type=None):
        if super(JsonStack, self).__len__() == 0:
            raise JsonStackError("The stack is empty.No popping.",
                                 "Popping item")
        item = super(JsonStack, self).pop()
        if item_type is None or item.is_type(item_type):
            return item
        raise JsonStackError("Type is not match.", "Popping item.")

    def is_empty(self):
        return super(JsonStack, self).__len__() == 0
