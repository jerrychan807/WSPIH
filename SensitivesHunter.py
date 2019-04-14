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

    def startHunt(self):
        self.crawlLinks()  # 爬取链接
        self.prepare(self.links_crawler.subdomain_name)
        self.saveLinksInFile(self.links_crawler.file_links, self.links_crawler.other_links)

    def prepare(self, subdomain_name):
        '''
         
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

    def downloadFile(self, url_file_list):

        download = DownLoader(self.domain_path, url_file_list, file_type)
        download.prepare()
        result = download.startDownload()


if __name__ == '__main__':
    url = 'http://wenfa.sdau.edu.cn'
    project_name = 'tmp'
    hunter = SensitivesHunter(url, project_name)
    hunter.startHunt()
