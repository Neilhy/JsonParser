#! /usr/bin/env python
# -*- coding:utf-8 -*-

import jsonerror
import jsonstack
from jsonstack import StackItem
from tokenreader import TokenReader
from tokenreader import TokenType


class JsonReader(object):
    """
    To read json from TokenReader and check the grammar of json
    """

    EXPECT_OBJECT_KEY = 1  # XXX :
    EXPECT_OBJECT_VALUE = 1 << 1  # : XXX
    EXPECT_OBJECT_BEGIN = 1 << 2  # {
    EXPECT_OBJECT_END = 1 << 3  # }
    EXPECT_LIST_VALUE = 1 << 4  # [XX,XX]
    EXPECT_LIST_BEGIN = 1 << 5  # [
    EXPECT_LIST_END = 1 << 6  # ]
    EXPECT_COMMA = 1 << 7  # ,
    EXPECT_COLON = 1 << 8  # :
    EXPECT_DOC_END = 1 << 9  # EOF
    EXPECT_VALUE = 1 << 10  # bool,string,number,null

    def __init__(self, reader):
        self.token_reader = TokenReader(reader)
        self.json_stack = jsonstack.JsonStack()

    def json_read(self):
        expected_next_token = (
            JsonReader.EXPECT_OBJECT_BEGIN,
            JsonReader.EXPECT_LIST_BEGIN,
            JsonReader.EXPECT_VALUE
        )
        while True:
            current_token = self.token_reader.read_next_token()
            if current_token == TokenType.START_OBJ:
                if JsonReader.EXPECT_OBJECT_BEGIN in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_OBJECT, dict())
                    )
                    expected_next_token = (
                        JsonReader.EXPECT_OBJECT_KEY,
                        JsonReader.EXPECT_OBJECT_END
                    )
                else:
                    raise jsonerror.JsonParseError(
                        "Unexpected '{' .", "Json_read:START_OBJ.")

            elif current_token == TokenType.START_LIST:
                if JsonReader.EXPECT_LIST_BEGIN in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_LIST, list())
                    )
                    expected_next_token = (
                        JsonReader.EXPECT_LIST_END,
                        JsonReader.EXPECT_LIST_VALUE,
                        JsonReader.EXPECT_LIST_BEGIN,
                        JsonReader.EXPECT_OBJECT_BEGIN
                    )
                else:
                    raise jsonerror.JsonParseError(
                        "Unexpected '['.", "Json_read:START_LIST.")

            elif current_token == TokenType.END_OBJ:
                if JsonReader.EXPECT_OBJECT_END in expected_next_token:
                    stack_item = self.json_stack.pop(StackItem.TYPE_JSON_OBJECT)
                    if self.json_stack.is_empty():  # Reach to the EOF:{...}
                        self.json_stack.push(stack_item)
                        expected_next_token = (JsonReader.EXPECT_DOC_END,)
                        continue
                    else:
                        stack_item_pre = self.json_stack.pop()
                        # { xx:{...}}
                        if stack_item_pre.get_item_type() == StackItem.TYPE_JSON_OBJECT_KEY:
                            item_value_key = stack_item_pre.get_item_value()

                            stack_item_pre_dict = self.json_stack.pop(
                                StackItem.TYPE_JSON_OBJECT)
                            stack_item_pre_dict.get_item_value()[
                                item_value_key] = stack_item

                            self.json_stack.push(stack_item_pre_dict)
                            expected_next_token = (
                                JsonReader.EXPECT_COMMA,
                                JsonReader.EXPECT_OBJECT_END
                            )
                            continue
                        # [ ,{...}, ]
                        elif stack_item_pre.get_item_type() == StackItem.TYPE_JSON_LIST:
                            item_value_list = stack_item_pre.get_item_value()
                            item_value_list.append(stack_item)

                            self.json_stack.push(stack_item_pre)
                            expected_next_token = (
                                JsonReader.EXPECT_COMMA,
                                JsonReader.EXPECT_LIST_END
                            )
                            continue
                raise jsonerror.JsonParseError("Unexpected '}'.",
                                               "Json_read:END_OBJ.")
            elif current_token == TokenType.END_LIST:
                if JsonReader.EXPECT_LIST_END in expected_next_token:
                    stack_item = self.json_stack.pop(StackItem.TYPE_JSON_LIST)
                    if self.json_stack.is_empty():  # Reach to the EOF:[...]
                        self.json_stack.push(stack_item)
                        expected_next_token = (JsonReader.EXPECT_DOC_END,)
                        continue
                    else:
                        stack_item_pre = self.json_stack.pop()
                        # { xx:[...]}
                        if stack_item_pre.get_item_type() == StackItem.TYPE_JSON_OBJECT_KEY:
                            item_value_key = stack_item_pre.get_item_value()

                            stack_item_pre_dict = self.json_stack.pop(
                                StackItem.TYPE_JSON_OBJECT)
                            stack_item_pre_dict.get_item_value()[
                                item_value_key] = stack_item

                            self.json_stack.push(stack_item_pre_dict)
                            expected_next_token = (
                                JsonReader.EXPECT_COMMA,
                                JsonReader.EXPECT_OBJECT_END
                            )
                            continue
                        # [ ,[...], ]
                        elif stack_item_pre.get_item_type() == StackItem.TYPE_JSON_LIST:
                            item_value_list = stack_item_pre.get_item_value()
                            item_value_list.append(stack_item)

                            self.json_stack.push(stack_item_pre)
                            expected_next_token = (
                                JsonReader.EXPECT_COMMA,
                                JsonReader.EXPECT_LIST_END
                            )
                            continue
                raise jsonerror.JsonParseError("Unexpected '}'.",
                                               "Json_read:END_LIST.")

            elif current_token == TokenType.COLON:
                if JsonReader.EXPECT_COLON in expected_next_token:
                    expected_next_token = (
                        JsonReader.EXPECT_OBJECT_VALUE,
                        JsonReader.EXPECT_OBJECT_BEGIN,
                        JsonReader.EXPECT_LIST_BEGIN
                    )
                else:
                    raise jsonerror.JsonParseError("Unexpected ':' .",
                                                   "Json_read:COLON")

            elif current_token == TokenType.COMMA:
                if JsonReader.EXPECT_COMMA in expected_next_token:
                    if JsonReader.EXPECT_OBJECT_END in expected_next_token:  # {,}
                        expected_next_token = (
                            JsonReader.EXPECT_OBJECT_KEY,
                        )
                        continue
                    elif JsonReader.EXPECT_LIST_END in expected_next_token:  # [,]
                        expected_next_token = (
                            JsonReader.EXPECT_LIST_BEGIN,
                            JsonReader.EXPECT_OBJECT_BEGIN,
                            JsonReader.EXPECT_LIST_VALUE
                        )
                        continue
                raise jsonerror.JsonParseError("Unexpected ',' .",
                                               "Json_read:COMMA")

            elif current_token == TokenType.BOOL:
                bool_value = self.token_reader.read_bool()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_VALUE, bool_value))
                    expected_next_token = (JsonReader.EXPECT_DOC_END,)
                elif JsonReader.EXPECT_OBJECT_VALUE in expected_next_token:
                    stack_item = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT_KEY)
                    stack_item_pre_dict = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT)

                    stack_item_pre_dict.get_item_value()[
                        stack_item.get_item_value()] = bool_value
                    self.json_stack.push(stack_item_pre_dict)

                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_OBJECT_END
                    )
                elif JsonReader.EXPECT_LIST_VALUE in expected_next_token:
                    stack_item_pre_list = self.json_stack.pop(
                        StackItem.TYPE_JSON_LIST)

                    stack_item_pre_list.get_item_value().append(bool_value)
                    self.json_stack.push(stack_item_pre_list)

                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_LIST_END
                    )
                else:
                    raise jsonerror.JsonParseError("Unexpected bool.",
                                                   "Json_read:BOOL")

            elif current_token == TokenType.NUMBER:
                number_value = self.token_reader.read_number()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_VALUE, number_value))
                    expected_next_token = (
                        JsonReader.EXPECT_DOC_END,
                    )
                elif JsonReader.EXPECT_OBJECT_VALUE in expected_next_token:
                    stack_item = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT_KEY)
                    stack_item_pre_dict = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT)

                    stack_item_pre_dict.get_item_value()[
                        stack_item.get_item_value()] = number_value
                    self.json_stack.push(stack_item_pre_dict)
                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_OBJECT_END
                    )
                elif JsonReader.EXPECT_LIST_VALUE in expected_next_token:
                    stack_item_pre_list = self.json_stack.pop(
                        StackItem.TYPE_JSON_LIST)

                    stack_item_pre_list.get_item_value().append(number_value)
                    self.json_stack.push(stack_item_pre_list)

                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_LIST_END
                    )
                else:
                    raise jsonerror.JsonParseError("Unexpected number.",
                                                   "Json_read:NUMBER")

            elif current_token == TokenType.NULL:
                self.token_reader.read_null()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_VALUE, None))
                    expected_next_token = (
                        JsonReader.EXPECT_DOC_END,
                    )
                elif JsonReader.EXPECT_OBJECT_VALUE in expected_next_token:
                    stack_item = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT_KEY)
                    stack_item_pre_dict = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT)

                    stack_item_pre_dict.get_item_value()[
                        stack_item.get_item_value()] = None
                    self.json_stack.push(stack_item_pre_dict)
                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_OBJECT_END
                    )
                elif JsonReader.EXPECT_LIST_VALUE in expected_next_token:
                    stack_item_pre_list = self.json_stack.pop(
                        StackItem.TYPE_JSON_LIST)

                    stack_item_pre_list.get_item_value().append(None)
                    self.json_stack.push(stack_item_pre_list)

                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_LIST_END
                    )
                else:
                    raise jsonerror.JsonParseError("Unexpected null.",
                                                   "Json_read:NULL")

            elif current_token == TokenType.STRING:
                string_value = self.token_reader.read_string()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_VALUE,
                                  unicode(string_value)))
                    expected_next_token = (
                        JsonReader.EXPECT_DOC_END,
                    )
                elif JsonReader.EXPECT_OBJECT_KEY in expected_next_token:
                    self.json_stack.push(
                        StackItem(StackItem.TYPE_JSON_OBJECT_KEY,
                                  unicode(string_value))
                    )
                    expected_next_token = (
                        JsonReader.EXPECT_COLON,
                    )
                elif JsonReader.EXPECT_OBJECT_VALUE in expected_next_token:
                    stack_item = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT_KEY)
                    stack_item_pre_dict = self.json_stack.pop(
                        StackItem.TYPE_JSON_OBJECT)

                    stack_item_pre_dict.get_item_value()[
                        stack_item.get_item_value()] = unicode(string_value)
                    self.json_stack.push(stack_item_pre_dict)
                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_OBJECT_END
                    )
                elif JsonReader.EXPECT_LIST_VALUE in expected_next_token:
                    stack_item_pre_list = self.json_stack.pop(
                        StackItem.TYPE_JSON_LIST)

                    stack_item_pre_list.get_item_value().append(string_value)
                    self.json_stack.push(stack_item_pre_list)

                    expected_next_token = (
                        JsonReader.EXPECT_COMMA,
                        JsonReader.EXPECT_LIST_END
                    )
                else:
                    raise jsonerror.JsonParseError("Unexpected string '\"''.",
                                                   "Json_read:STRING")
            elif current_token == TokenType.END_DOC:
                if JsonReader.EXPECT_DOC_END in expected_next_token:
                    stack_item_last = self.json_stack.pop()
                    if self.json_stack.is_empty():
                        return self.stack_item_to_json_data(stack_item_last)
                raise jsonerror.JsonParseError("Unexpected JSON_END.",
                                               "Json_read:END_DOC")

    def stack_item_to_json_data(self, json_root):
        item_type = json_root.get_item_type()
        if item_type in (StackItem.TYPE_JSON_OBJECT, StackItem.TYPE_JSON_LIST):
            return self.stack_item_to_json_arr_or_dict(json_root)
        elif item_type == StackItem.TYPE_JSON_VALUE:
            return json_root.get_item_value()

    def stack_item_to_json_arr_or_dict(self, json_root):
        item_type = json_root.get_item_type()
        if item_type == StackItem.TYPE_JSON_OBJECT:
            to_parent = dict()
            for dict_item in json_root.get_item_value().items():
                dict_key = dict_item[0]
                dict_value = dict_item[1]
                if isinstance(dict_value, StackItem):
                    dict_value = self.stack_item_to_json_arr_or_dict(dict_value)
                to_parent[dict_key] = dict_value
            return to_parent
        elif item_type == StackItem.TYPE_JSON_LIST:
            to_parent = list()
            for list_item in json_root.get_item_value():
                if isinstance(list_item, StackItem):
                    list_item = self.stack_item_to_json_arr_or_dict(list_item)
                to_parent.append(list_item)
            return to_parent
