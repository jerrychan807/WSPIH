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
        self.saved_file_path_list = []

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
            r = requests.get(file_url, headers=headers, verify=False)

            # print(r.status_code) # debug时使用

            if str(r.status_code).startswith('2'):
                with open(saved_file_path, "wb") as xls_file:
                    xls_file.write(r.content)
                return saved_file_path
        except Exception as e:
            log.logger.debug(e)
        return ''

    def startDownload(self):
        executor = ThreadPoolExecutor(max_workers=5)
        all_task = [executor.submit(self.download, (url)) for url in self.url_list]
        for future in as_completed(all_task):
            saved_file_path = future.result()
            if saved_file_path:
                self.saved_file_path_list.append(saved_file_path)
        return self.saved_file_path_list


if __name__ == '__main__':
    url_list = [
        'http://wenfa.sdau.edu.cn/_upload/article/files/5d/c8/490da6e14e568f347c5f8c7b3ea0/b10e7574-7854-442e-9dc1-0bed27be0720.xlsx',
        'http://wenfa.sdau.edu.cn/_upload/article/files/67/8b/059cb8444ac4a09d0e9b662c3d9f/722014e3-962b-4cf9-8a75-054b726cb54d.xlsx',
        'http://wenfa.sdau.edu.cn/_upload/article/files/67/8b/059cb8444ac4a09d0e9b662c3d9f/722014e3-962b-4cf9-8a75-054b726cb541d.xlsx']
    project_path = 'tmp/wenfa.sdau.edu.cn'
    file_type = 'excel'
    download = DownLoader(project_path, url_list, file_type)
    download.prepare()
    result = download.startDownload()
    print(result)
