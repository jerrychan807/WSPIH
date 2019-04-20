#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/9 10:12 PM
# @Author  : Jerry
# @Desc    : 读取一个文件
# @File    : ExcelParser.py

import xlrd

from lib.parser.BaseParser import BaseParser


class ExcelParser(BaseParser):
    def read(self):
        workbook = xlrd.open_workbook(self.file_path)
        all_sheet_name = workbook.sheet_names()

        for sheet_name in all_sheet_name:
            sheet = workbook.sheet_by_name(sheet_name)
            nrows = sheet.nrows
            if nrows == 0:
                continue

            for rownum in range(nrows):
                for cell_value in sheet.row_values(rownum):
                    if cell_value:
                        cell_value = str(cell_value).strip()
                        idcard_result = self.idcard_search(cell_value)
                        if idcard_result:
                            self.sensitive_dict['idcard'].append(idcard_result)

                        phone_result = self.phone_search(cell_value)
                        if phone_result:
                            self.sensitive_dict['phone'].append(phone_result)

                        email_result = self.email_search(cell_value)
                        if email_result:
                            self.sensitive_dict['email'].append(email_result)

        self.reduce_error_report()
        return self.sensitive_dict
