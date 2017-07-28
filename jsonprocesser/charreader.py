#! /usr/bin/env python
# -*- coding:utf-8 -*-


import jsonerror


class CharReader(object):
    BUFFER_SIZE = 10

    def __init__(self, json_string):
        self.buffer = []
        self.had_read = 0
        self.pos = 0
        self.string_pos = 0
        self.buffer_size = 0
        self.json_string = json_string

    def has_more_char(self):
        if self.pos < self.buffer_size:
            return True
        self.read_into_buffer(None)
        return self.pos < self.buffer_size

    def read_into_buffer(self, eof_msg):
        string = self._read(self.BUFFER_SIZE)
        self.buffer = list(string)
        if not self.buffer:
            if eof_msg is not None:
                raise jsonerror.JsonEOFError(eof_msg, "In CharReader")
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

    def _read(self, buf_size):
        pre_pos = self.string_pos
        if self.string_pos + buf_size >= len(self.json_string):
            self.string_pos = len(self.json_string)
        else:
            self.string_pos += buf_size
        return self.json_string[pre_pos:self.string_pos]
