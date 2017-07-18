#! /usr/bin/env python
# -*- coding:utf-8 -*-


class StringReader(object):
    def __init__(self, string):
        self.string = string
        self.pos = 0
        self.string_len = len(string)

    def read(self, buf_size):
        pre_pos = self.pos
        if self.pos + buf_size >= self.string_len:
            self.pos = self.string_len
        else:
            self.pos += buf_size
        return self.string[pre_pos:self.pos]

#
# sr = StringReader("123456789")
# while True:
#     str1 = sr.read(2)
#     if not str1:
#         break
#     print str1
