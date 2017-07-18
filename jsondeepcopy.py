#! /usr/bin/env python
# -*- coding:utf -*-


class JsonDeepCopy(object):
    """
    To deep copy the json_value
    """
    def copy_deep(self, value):
        if isinstance(value, dict):
            new_dict = dict()
            for k, v in value.items():
                if isinstance(k, str):
                    new_dict[k] = self.copy_deep(v)
            return new_dict
        elif isinstance(value, list):
            new_list = list()
            for lst in value:
                new_list.append(lst)
            return new_list
        else:
            return value


# v1 = 123
# v2 = "abc"
# v3 = None
# v4 = True
# v5 = {"1": 1}
# v6 = [1, 2, 3]
# 
# jdc = JsonDeepCopy()
# print v1 == jdc.copy_deep(v1), v1 is jdc.copy_deep(v1)
# print v2 == jdc.copy_deep(v2), v2 is jdc.copy_deep(v2)
# print v3 == jdc.copy_deep(v3), v3 is jdc.copy_deep(v3)
# print v4 == jdc.copy_deep(v4), v4 is jdc.copy_deep(v4)
# print v5 == jdc.copy_deep(v5), v5 is jdc.copy_deep(v5), jdc.copy_deep(v5)
# print v6 == jdc.copy_deep(v6), v6 is jdc.copy_deep(v6), jdc.copy_deep(v6)
