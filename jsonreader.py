#! /usr/bin/env python
# -*- coding:utf -*-

import tokenreader
import jsonstack
from token import TokenType
from stackitem import StackItem
from parseerror import ParseError


class JsonReader(object):
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
    EXPECT_VALUE = 1<<10  # bool,string,number,null

    def __init__(self, json_string):
        self.token_reader = tokenreader.TokenReader(json_string)
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
                        StackItem(StackItem.TYPE_JSON_OBJECT_BEGIN, dict())
                    )
                    expected_next_token = (
                        JsonReader.EXPECT_OBJECT_KEY,
                        JsonReader.EXPECT_OBJECT_END
                    )
                else:
                    raise ParseError(
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
                    raise ParseError(
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
                            stack_item_pre_dict.get_item_value()[item_value_key] = stack_item

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
                raise ParseError("Unexpected '}'.", "Json_read:END_OBJ.")
            elif current_token == TokenType.END_LIST:
                if JsonReader.EXPECT_LIST_END in expected_next_token:
                    stack_item = self.json_stack.pop(StackItem.TYPE_JSON_OBJECT)
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
                            stack_item_pre_dict.get_item_value()[item_value_key] = stack_item

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
                raise ParseError("Unexpected '}'.", "Json_read:END_LIST.")

            elif current_token == TokenType.COLON:
                if JsonReader.EXPECT_COLON in expected_next_token:
                    expected_next_token = (
                        JsonReader.EXPECT_OBJECT_VALUE,
                        JsonReader.EXPECT_OBJECT_BEGIN,
                        JsonReader.EXPECT_LIST_BEGIN
                    )
                else:
                    raise ParseError("Unexpected ':' .", "Json_read:COLON")

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
                raise ParseError("Unexpected ',' .", "Json_read:COMMA")

            elif current_token == TokenType.BOOL:
                bool_value = self.token_reader.read_boolean()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(StackItem.create_json_value(bool_value))
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
                    raise ParseError("Unexpected bool.", "Json_read:BOOL")

            elif current_token == TokenType.NUMBER:
                number_value = self.token_reader.read_number()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(StackItem.create_json_value(number_value))
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
                    raise ParseError("Unexpected number.", "Json_read:NUMBER")

            elif current_token == TokenType.NULL:
                self.token_reader.read_null()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem.create_json_value(None))
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
                    raise ParseError("Unexpected null.", "Json_read:NULL")

            elif current_token == TokenType.STRING:
                string_value = self.token_reader.read_string()

                if JsonReader.EXPECT_VALUE in expected_next_token:
                    self.json_stack.push(
                        StackItem.create_json_value(string_value))
                    expected_next_token = (
                        JsonReader.EXPECT_DOC_END,
                    )
                elif JsonReader.EXPECT_OBJECT_KEY in expected_next_token:
                    self.json_stack.push(
                        StackItem.create_json_object_key(string_value)
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
                        stack_item.get_item_value()] = string_value
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
                    raise ParseError("Unexpected string '\"''.",
                                     "Json_read:STRING")
            elif current_token == TokenType.END_DOC:
                if JsonReader.EXPECT_DOC_END in expected_next_token:
                    stack_item_last = self.json_stack.pop()
                    if self.json_stack.is_empty():
                        return stack_item_last.get_item_value()
                raise ParseError("Unexpected JSON_END.", "Json_read:END_DOC")
