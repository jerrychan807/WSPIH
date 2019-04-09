#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/9 10:35 PM
# @Author  : Jerry
# @Desc    : 
# @File    : test_excelparser.py

import unittest
from lib.parser.ExcelParser import ExcelParser


class TestExcelParser(unittest.TestCase):
    file_path = 'data/1.xls'
    excel_parser = ExcelParser(file_path)

    def test_get_idcard(self):
        self.excel_parser.read()
        print(self.excel_parser.sensitive_dict)

if __name__ == '__main__':
    unittest.main()
