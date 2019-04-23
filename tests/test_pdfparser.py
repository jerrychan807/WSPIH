#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jack
# datetime:2019-04-10 16:05
# software: PyCharm

import unittest
from lib.parser.PdfParser import PdfParser


class TestPDFParser(unittest.TestCase):
    file_path = 'data/pdf.pdf'
    PDF_parser = PdfParser(file_path)

    def test_get_idcard(self):
        self.PDF_parser.read()
        print(self.PDF_parser.sensitive_dict)

if __name__ == '__main__':
    unittest.main()