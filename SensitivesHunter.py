#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/10 10:10 PM
# @Author  : Jerry
# @Desc    : 
# @File    : SensitivesHunter.py

import json
import os
import sys
import subprocess

from lib.common.basic import getCurrentPath, makeDir, getDomain
from Downloader import DownLoader
from SensitiveFileParser import SensitiveFileParser


class SensitivesHunter():
    def __init__(self, url, project_name):
        self.start_url = url
        self.project_name = project_name
        self.crawled_file_links_dict = {}
        self.result_dict = {}

    def startHunt(self):
        self.prepare()
        self.crawlLinks()  # 爬取链接
        # self.saveLinksInFile(self.links_crawler.file_links, self.links_crawler.other_links)
        self.parseFileLinks()  # 解析爬取到的文件url
        for file_type, url_file_list in self.crawled_file_links_dict.items():
            downloaded_file_path_list = self.downloadFile(url_file_list, file_type)
            self.detectSensitiveFile(downloaded_file_path_list, file_type)
        self.saveResultFile()

    def prepare(self):
        '''
        创建存放的文件夹和文件
        '''

        self.current_path = getCurrentPath()
        project_path = os.path.join(self.current_path, self.project_name)
        makeDir(project_path)
        subdomain_name = getDomain(self.start_url)
        self.domain_path = os.path.join(project_path, subdomain_name)
        makeDir(self.domain_path)
        self.file_links_path = os.path.join(self.domain_path, 'file_links.json')
        # self.other_links_path = os.path.join(self.domain_path, 'other_links.json')
        self.finally_result_path = os.path.join(self.domain_path, 'result.json')

    def crawlLinks(self):
        '''
        爬取链接
        '''
        cmd = 'python3 ' + '{0}/LinksCrawler.py {1} {2}'.format(self.current_path,
                                                                self.start_url, self.file_links_path, )
        print("[*] cmd: {}".format(cmd))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdoutput, erroutput) = p.communicate()

    def saveLinksInFile(self, file_links, other_links):
        '''
        将链接保存在文件中
        '''

        with open(self.file_links_path, "w") as f1:
            f1.write(str(json.dumps(file_links)))
            # with open(self.other_links_path, "w") as f2:
            #     f2.write(str(json.dumps(other_links)))

    def parseFileLinks(self):
        '''
        解析爬取到的文件url
        '''
        if os.path.exists(self.file_links_path):
            with open(self.file_links_path, 'r') as f:
                print('[*] reading {0}'.format(self.file_links_path))
                self.crawled_file_links_dict = json.load(f)
                # os.remove(self.file_links_path)  # 删除

    def downloadFile(self, url_file_list, file_type):
        '''
        下载文件
        '''
        download = DownLoader(self.domain_path, url_file_list, file_type)
        # download.prepare()
        downloaded_file_path = download.startDownload()
        return downloaded_file_path

    def detectSensitiveFile(self, downloaded_file_path_list, file_type):
        '''
        检测含敏感信息的文件
        :param file_type: 文件类型 
        :return: 
        '''
        parser = SensitiveFileParser(downloaded_file_path_list, file_type)
        sensitive_result_dict = parser.startParse()
        if sensitive_result_dict:
            self.result_dict = dict(sensitive_result_dict.items())

    def saveResultFile(self):
        '''
        保存最终结果 
        '''

        if len(self.result_dict):
            with open(self.finally_result_path, "w") as f:
                f.write(str(json.dumps(self.result_dict)))


def main(target_txt, project_name):
    with open(target_txt, 'r') as f:
        url_list = [url.strip() for url in f]
    print("[*] target length is :{}".format(len(url_list)))
    for url in url_list:
        hunter = SensitivesHunter(url, project_name)
        hunter.startHunt()


if __name__ == '__main__':
    # url = 'http://wenfa.sdau.edu.cn'
    # project_name = 'tmp'
    target_txt = sys.argv[1]
    project_name = sys.argv[2] if sys.argv[2] else 'tmp'
    main(target_txt, project_name)
