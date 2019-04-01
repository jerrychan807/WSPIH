#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/1 4:46 PM
# @Author  : Jerry
# @Desc    : 
# @File    : test_urlhelper.py


import unittest
from lib.third.nyawc.helpers.URLHelper import URLHelper


class TestUrlHelper(unittest.TestCase):
    __host = ""
    __urls = ["http://www.gjjlhzc.ccut.edu.cn/2018/1129/c2956a59091/page.htm",
              "http://gqt.dept.ccut.edu.cn/picright.asp?id=468",
              "http://stlhh.zt.ccut.edu.cn",
              "http://www.baidu.com",
              "http://mse.sysu.edu.cn/"]

    def test_get_hostname(self):
        print('test host name')
        for url in self.__urls:
            print("{0} --> {1}".format(url, URLHelper.get_hostname(url)))

    def test_get_subdmoain(self):
        print('test subdomain')
        for url in self.__urls:
            print("{0} --> {1}".format(url, URLHelper.get_subdomain(url)))


if __name__ == '__main__':
    unittest.main()
