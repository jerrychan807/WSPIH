#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jack
# datetime:2019-04-10 16:05
# software: PyCharm

import unittest
from lib.parser.PdfParser import PDF_Parser


class TestPDFParser(unittest.TestCase):
    file_path = 'data/pdf.pdf'
    PDF_parser = PDF_Parser(file_path)

    def test_get_idcard(self):
        self.PDF_parser.read()
        print(self.PDF_parser.sensitive_dict)

if __name__ == '__main__':
    unittest.main()