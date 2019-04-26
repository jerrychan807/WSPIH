#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/8 16:15
# @Author  : Jerry
# @Desc    : 给定任意url,将下载后的内容保存在指定的路径里
# @File    : Downloader.py

from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os

requests.packages.urllib3.disable_warnings()

from lib.config import log
from lib.common.basic import makeDir

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}


class DownLoader():
    def __init__(self, domain_path, url_list, file_type):
        self.domain_path = domain_path
        self.url_list = url_list
        self.file_type = file_type
        self.saved_file_path_dict = {}

    def getFileName(self, file_url):
        file_name = file_url.split("/")[-1]
        return file_name.strip()

    # def prepare(self):
    #     self.saved_folder_path = os.path.join(self.domain_path, self.file_type)
    #     self.saved_folder_path = os.path.join(self.domain_path, self.file_type)
    #     makeDir(self.saved_folder_path)

    # @exception(log.logger)
    def download(self, file_url):
        file_name = self.getFileName(file_url)

        saved_file_path = os.path.join(self.domain_path, file_name)

        try:
            r = requests.get(file_url, headers=headers, verify=False, timeout=20)
            # 当未指定超时时间时，默认的超时时间是 None，亦即连接永远不会超时。 refs:https://segmentfault.com/q/1010000004935548
            # print(r.status_code) # debug时使用

            if str(r.status_code).startswith('2'):
                with open(saved_file_path, "wb") as xls_file:
                    xls_file.write(r.content)
                return file_url, saved_file_path
        except Exception as e:
            pass  # 报错日志过多
            # log.logger.debug(e)
        return '', ''

    def startDownload(self):
        executor = ThreadPoolExecutor(max_workers=10)  # 并发下载
        all_task = [executor.submit(self.download, (url)) for url in self.url_list]
        for future in as_completed(all_task):
            file_url, saved_file_path = future.result()
            if saved_file_path:
                self.saved_file_path_dict[file_url] = saved_file_path
        return self.saved_file_path_dict
