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


if __name__ == '__main__':
    downloaded_file_path_list = [
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/b9540a5e-4fb8-4dea-aa87-ea56b974e2ec.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/33c4330c-a67b-491b-b0ca-b1b4a5c02f0d.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/efa98140-928d-4ec8-ad29-429a59f09440.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/5b878370-cf4e-4b7c-b296-6903fe8daa3d.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/5ecc6249-85e1-439e-9eff-562b112bb1f5.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/78cf8308-95a6-486c-95e9-410828dcb9c5.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/0e7fe3ed-98d2-48c3-a9dd-8b035af51922.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/3088454d-b442-46d0-aa52-21c67a5a0d67.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/1886776f-8381-4106-a443-8c3662f26e77.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/e59a5380-0de1-41ed-9c1b-c348848e479b.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/a2a9b54d-2d6d-4018-a5da-34e08ae18a37.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/7f6c2cd3-eeb0-4f50-92a9-b12b2bfccce0.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/7db7c9f3-2cb3-48ab-ada2-0b04eaafae29.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/dc17ae5a-707a-42ea-b067-8bea882c98d3.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/2b543787-e2ac-46d5-9942-97961e86ddcf.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/97b2384e-75b0-452e-8267-cab351890170.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/9fc58324-cef3-4a73-a837-5c3814b2e182.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/ce1feb6a-6efe-449a-99f9-484aa1b0e04c.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/b1f34182-02b3-4d57-aaae-18f809c6ff88.docx',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/c48a08fe-3a3a-45ee-a9a3-984220c980b9.doc',
        '/Users/chanjerry/Documents/GitHub/WSPIH/tmp/wenfa.sdau.edu.cn/word/3f400e95-275f-4ea0-a802-43cad8e17a43.doc']
    file_type = 'word'
    parser = SensitiveFileParser(downloaded_file_path_list, file_type)
    result = parser.startParse()
    print(result)
