#! /usr/bin/env python
# -*- coding:utf-8 -*-


import eoferror


class CharReader(object):
    BUFFER_SIZE = 10

    def __init__(self, reader):
        self.reader = reader
        self.buffer = []
        self.had_read = 0
        self.pos = 0
        self.buffer_size = 0

    def has_more_char(self):
        if self.pos < self.buffer_size:
            return True
        self.read_into_buffer(None)
        return self.pos < self.buffer_size

    def read_into_buffer(self, eof_msg):
        string = self.reader.read(self.BUFFER_SIZE)
        self.buffer = list(string)
        if not self.buffer:
            if eof_msg is not None:
                raise eoferror.JsonEOFError(eof_msg, "In CharReader")
            return
        self.pos = 0
        self.buffer_size = len(self.buffer)
        self.had_read += self.buffer_size

    def read_next_char(self):
        if self.pos == self.buffer_size:
            self.read_into_buffer("EOF of the file.")
        c = self.buffer[self.pos]
        self.pos += 1
        return c

    def read_top_char(self):
        if self.pos == self.buffer_size:
            self.read_into_buffer("EOF of the file.")
        return self.buffer[self.pos]
