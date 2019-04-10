#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jack
# datetime:2019-04-10 16:05
# software: PyCharm

import unittest
from lib.parser.WordParser import WordParser


class TestwordParser(unittest.TestCase):
    file_path = 'data/docx.docx'
    wordparserObj = WordParser(file_path)

    def test_get_idcard(self):
        self.wordparserObj.read()
        print(self.wordparserObj.sensitive_dict)


if __name__ == '__main__':
    unittest.main()
