#! /usr/bin/env python
# -*- coding:utf-8 -*-


class TokenType:
    """
    object
        {}
        { members }
    members
        pair
        pair , members
    pair
        string : value
    array
        []
        [ elements ]
    elements
        value
        value , elements
    value
        string
        number
        object
        array
        true
        false
        null
    string
        ""
        " chars "
    chars
        char
        char chars
    char
        any-Unicode-character-
        except-"-or-\-or-
        control-character
        \"
        \\
        \/
        \b
        \f
        \n
        \r
        \t
        \u four-hex-digits
    number
        int
        int frac
        int exp
        int frac exp
    """
    START_OBJ = 1
    END_OBJ = 2
    START_LIST = 3
    END_LIST = 4
    NULL = 5
    NUMBER = 6
    STRING = 7
    BOOL = 8
    COLON = 9
    COMMA = 10
    END_DOC = 11
