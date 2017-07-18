#! /usr/bin/env python
# -*- coding:utf-8 -*-


class FileReader(object):
    def __init__(self, file_name):
        self.file = open(file_name)

    def read(self, buf_size):
        return self.file.read(buf_size)

#
# fr = FileReader("E:/json.txt")
# while True:
#     str1 = fr.read(10)
#     if not str1:
#         break
#     print str1
