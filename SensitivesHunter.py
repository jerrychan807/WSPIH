#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/10 10:10 PM
# @Author  : Jerry
# @Desc    : 
# @File    : SensitivesHunter.py

import json
import os

from LinksCrawler import LinksCrawler
from Downloader import DownLoader
from lib.common.basic import getCurrentPath, makeDir


class SensitivesHunter():
    def __init__(self, url, project_name):
        self.start_url = url
        self.project_name = project_name
        self.crawled_file_links_dict = {}

    def startHunt(self):
        self.crawlLinks()  # 爬取链接
        self.prepare(self.links_crawler.subdomain_name)
        self.saveLinksInFile(self.links_crawler.file_links, self.links_crawler.other_links)
        self.parseFileLinks() # 解析爬取到的文件url
        for file_type, url_file_list in self.crawled_file_links_dict.items():
            self.downloadFile(url_file_list, file_type)

    def prepare(self, subdomain_name):
        '''
        创建存放的文件夹和文件
        '''
        current_path = getCurrentPath()
        project_path = os.path.join(current_path, self.project_name)
        makeDir(project_path)
        self.domain_path = os.path.join(project_path, subdomain_name)
        makeDir(self.domain_path)
        self.file_links_path = os.path.join(self.domain_path, 'file_links.json')
        self.other_links_path = os.path.join(self.domain_path, 'other_links.json')

    def crawlLinks(self):
        '''
        爬取链接
        '''
        self.links_crawler = LinksCrawler(self.start_url)
        self.links_crawler.prepare()
        self.links_crawler.setOptions()
        self.links_crawler.startCrawl()
        # print(self.links_crawler.file_links)

    def saveLinksInFile(self, file_links, other_links):
        '''
        将链接保存在文件中
        '''

        with open(self.file_links_path, "w") as f1:
            f1.write(str(json.dumps(file_links)))
        with open(self.other_links_path, "w") as f2:
            f2.write(str(json.dumps(other_links)))

    def parseFileLinks(self):
        '''
        解析爬取到的文件url
        '''
        if os.path.exists(self.file_links_path):
            with open(self.file_links_path, 'r') as f:
                print('[*] reading {0}'.format(self.file_links_path))
                self.crawled_file_links_dict = json.load(f)
                os.remove(self.file_links_path)  # 删除

    def downloadFile(self, url_file_list, file_type):
        '''
        下载文件
        '''
        download = DownLoader(self.domain_path, url_file_list, file_type)
        download.prepare()
        result = download.startDownload()
        print(result)

    def detectSensitiveFile(self, file_type):
        pass


if __name__ == '__main__':
    url = 'http://wenfa.sdau.edu.cn'
    project_name = 'tmp'
    hunter = SensitivesHunter(url, project_name)
    hunter.startHunt()
