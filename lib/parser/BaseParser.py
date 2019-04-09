#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/3 11:25 PM
# @Author  : Jerry
# @Desc    : 
# @File    : BaseParser.py

import re
from lib.utils.regex import PHONE_REGEX, EMAIL_REGEX, IDCARD_REGEX


class BaseParser():
    def __init__(self, file_path):
        self.file_path = file_path
        self.sensitive_dict = {'phone': [], 'idcard': [], 'email': []}

    @classmethod
    def re_search(cls, regex_patern, item_value):
        result = re.search(regex_patern, item_value)
        if result:
            return result.group()

    @classmethod
    def phone_search(cls, item_value):
        return cls.re_search(PHONE_REGEX, item_value)

    @classmethod
    def idcard_search(cls, item_value):
        return cls.re_search(IDCARD_REGEX, item_value)

    @classmethod
    def email_search(cls, item_value):
        return cls.re_search(EMAIL_REGEX, item_value)
