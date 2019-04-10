#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/9 11:26 PM
# @Author  : Jerry, Jack
# @Desc    : 
# @File    : WordParser.py
'''
only support .docx file recently
read local .dock file and check the sensitive words
'''

from lib.third import docx
from lib.parser.BaseParser import BaseParser


class wordParser(BaseParser):
    def read(self):
        file = docx.Document(self.file_path)
        for para in file.paragraphs:
            para = para.text
            idcard_result = self.idcard_search(para)
            if idcard_result:
                self.sensitive_dict['idcard'].append(idcard_result)

            phone_result = self.phone_search(para)
            if phone_result:
                self.sensitive_dict['phone'].append(phone_result)

            email_result = self.email_search(para)
            if email_result:
                self.sensitive_dict['email'].append(email_result)

        tables = file.tables
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    para = cell.text
                    idcard_result = self.idcard_search(para)
                    if idcard_result:
                        self.sensitive_dict['idcard'].append(idcard_result)

                    phone_result = self.phone_search(para)
                    if phone_result:
                        self.sensitive_dict['phone'].append(phone_result)

                    email_result = self.email_search(para)
                    if email_result:
                        self.sensitive_dict['email'].append(email_result)
        return self.sensitive_dict
