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

from lib.config import log
from lib.common.basic import getCurrentPath, makeDir, getDomain
from Downloader import DownLoader
from SensitiveFileParser import SensitiveFileParser


class SensitivesHunter():
    def __init__(self, url, project_name):
        self.start_url = url
        self.project_name = project_name
        self.crawled_file_links_dict = {}
        self.result_dict = {}
        self.skip_flag = False  # 跳过爬取的标志

    def startHunt(self):
        self.prepare()
        self.tryToSkipCrawled()
        if not self.skip_flag:
            self.crawlLinks()  # 爬取链接
            self.parseFileLinks()  # 解析爬取到的文件url
            for file_type, url_file_list in self.crawled_file_links_dict.items():
                downloaded_file_path_list = self.downloadFile(url_file_list, file_type)
                self.detectSensitiveFile(downloaded_file_path_list, file_type)
            self.saveResultFile()

    def tryToSkipCrawled(self):
        '''
        不重复爬取
        '''
        if os.path.exists(self.file_links_path):
            print("[*] skip this site {}".format(self.start_url))
            self.skip_flag = True

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
        print("[*] start to crawlLinks {}".format(self.start_url))
        cmd = 'python3 ' + '{0}/LinksCrawler.py {1} {2}'.format(self.current_path,
                                                                self.start_url, self.file_links_path)
        print("[*] cmd: {}".format(cmd))
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (stdoutput, erroutput) = p.communicate()
        except:
            log.logger.debug(erroutput)

    def parseFileLinks(self):
        '''
        解析爬取到的文件url
        '''
        print("[*] start to parseFileLinks")
        if os.path.exists(self.file_links_path):
            with open(self.file_links_path, 'r') as f:
                print('[*] reading {0}'.format(self.file_links_path))
                self.crawled_file_links_dict = json.load(f)
                # os.remove(self.file_links_path)  # 删除

    def downloadFile(self, url_file_list, file_type):
        '''
        下载文件
        '''
        print("[*] start to downloadFile {0} :{1}".format(file_type, len(url_file_list)))
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
        print("[*] start to detectSensitiveFile {0} :{1}".format(file_type, len(downloaded_file_path_list)))
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
