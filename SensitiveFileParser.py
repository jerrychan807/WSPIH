#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/20 4:52 PM
# @Author  : Jerry
# @Desc    : 根据文件类型进行相应的敏感信息解析
# @File    : SensitiveFileParser.py

from lib.config import log
from lib.common.basic import deleteFile
from lib.parser.ExcelParser import ExcelParser
from lib.parser.WordParser import WordParser
from lib.parser.PdfParser import PdfParser

parser_dict = {'excel': ExcelParser, 'word': WordParser, 'pdf': PdfParser}


class SensitiveFileParser():
    def __init__(self, downloaded_file_path_list, file_type):
        self.downloaded_file_path_list = downloaded_file_path_list
        self.file_type = file_type
        self.sensitive_result_dict = {}

    def startParse(self):
        '''
        开始解析 
        '''

        for file in self.downloaded_file_path_list:
            parser = parser_dict[self.file_type](file)
            sensitive_dict = {}
            delete_flag = 1
            try:
                sensitive_dict = parser.read()
            # print(sensitive_dict)
            except Exception as e:
                # 无法解析的情况
                log.logger.debug(e)
                log.logger.debug(file)
            else:
                if sensitive_dict['phone'] or sensitive_dict['idcard'] or sensitive_dict['email']:
                    self.sensitive_result_dict[file] = sensitive_dict
                    delete_flag = 0
            finally:
                if delete_flag:
                    deleteFile(file)

        return self.sensitive_result_dict
