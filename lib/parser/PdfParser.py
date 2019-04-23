#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/9 11:26 PM
# @Author  : Jerry , Jack
# @Desc    : 
# @File    : PdfParser.py

from lib.parser.BaseParser import BaseParser
import importlib
import sys
from urllib.request import urlopen

importlib.reload(sys)
from lib.third.pdfminer.pdfparser import PDFParser, PDFDocument
from lib.third.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from lib.third.pdfminer.converter import PDFPageAggregator
from lib.third.pdfminer.layout import LTTextBoxHorizontal, LAParams
from lib.third.pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class PdfParser(BaseParser):
    def read(self):
        # print(self.file_path)
        # 文件读取
        if r'://' in self.file_path:
            fp = urlopen(self.file_path, 'rb')
        else:
            fp = open(self.file_path, 'rb')
        parser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器，与文档对象
        parser.set_document(doc)
        doc.set_parser(parser)

        # 提供初始化密码，如果没有密码，就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDF，资源管理器，来共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释其对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 循环遍历列表，每次处理一个page内容
            # doc.get_pages() 获取page列表
            for page in doc.get_pages():
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
                # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
                # 想要获取文本就获得对象的text属性，
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        check_raw = x.get_text()
                        check_raw = str(check_raw).strip()
                        if check_raw:
                            idcard_result = self.idcard_search(check_raw)
                            if idcard_result:
                                self.sensitive_dict['idcard'].append(idcard_result)

                            phone_result = self.phone_search(check_raw)
                            if phone_result:
                                self.sensitive_dict['phone'].append(phone_result)

                            email_result = self.email_search(check_raw)
                            if email_result:
                                self.sensitive_dict['email'].append(email_result)
        fp.close()
        self.reduce_error_report()
        return self.sensitive_dict


