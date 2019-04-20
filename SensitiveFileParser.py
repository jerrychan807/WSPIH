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
                e += file
                log.logger.debug(e)
            else:
                if sensitive_dict['phone'] or sensitive_dict['idcard'] or sensitive_dict['email']:
                    self.sensitive_result_dict[file] = sensitive_dict
                    delete_flag = 0
            finally:
                if delete_flag:
                    deleteFile(file)

        return self.sensitive_result_dict


if __name__ == '__main__':
    downloaded_file_path_list = [
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/332dc38c-1bf9-4e8b-8d0b-090eef4083eb.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/1746b43c-4f2d-40de-b461-19416fddb363.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/02ac0de8-c0f0-4e4b-8553-c3b76e6053ba.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/12dcaf95-3c3e-48c8-98ab-c31b61fd3bb1.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/5163557b-25a4-4d22-b873-5f208a5bc54e.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/dc6455e2-0d88-4185-a01b-f7a9aa628be6.pdf',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/pdf/pdf.pdf']

    file_type = 'pdf'
    parser = SensitiveFileParser(downloaded_file_path_list, file_type)
    result = parser.startParse()
    print(result)
