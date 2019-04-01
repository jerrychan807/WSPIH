# !/usr/local/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'jerry'

import os, json
from lib.third.nyawc.Options import Options
from lib.third.nyawc.Crawler import Crawler
from lib.third.nyawc.CrawlerActions import CrawlerActions
from lib.third.nyawc.http.Request import Request


from rules.extension import IGNORED_EXTESIONS, EXCEL_EXTENSIONS, PDF_EXTENSIONS, WORD_EXTENSIONS

from lib.utils.basic import extension, getDomain, makedir
from collections import defaultdict


class LinksCrawler():
    def __init__(self, subdomain, project_name='tmp'):
        self.subdomain = subdomain
        self.project_name = project_name
        self.options = Options()
        self.crawled_urls_to_check_dups = []
        self.file_links = []
        self.other_links = defaultdict(list)

    def prepare(self):
        '''
        预处理url
        '''
        self.subdomain_url = 'http://' + self.subdomain if 'http' not in self.subdomain else self.subdomain
        self.domain = getDomain(self.subdomain_url)
        current_path = os.getcwd()
        project_path = os.path.join(current_path, self.project_name)
        self.reuslt_path = os.path.join(project_path, self.domain)
        makedir(self.reuslt_path)

        print(self.subdomain_url)
        print(self.domain)
        print(self.reuslt_path)

    def setOptions(self):
        self._setPerformanceOptions()
        self._setScopeOptions()
        self._setIdentityOptions()
        self._setIgnoredExtensions()
        self._setFocusExtensions()

    def _setPerformanceOptions(self):
        '''
        设置性能
        refs: https://tijme.github.io/not-your-average-web-crawler/latest/options_performance.html
        '''

        self.options.performance.max_threads = 20  # 线程
        self.options.performance.request_timeout = 30  # 超时时间

    def _setScopeOptions(self):
        '''
        设置作用域
        :return: 
        '''
        self.options.scope.protocol_must_match = False  # 协议
        self.options.scope.subdomain_must_match = False  # 子域名
        self.options.scope.hostname_must_match = True  # 主机名
        self.options.scope.tld_must_match = True  # 顶级域名
        self.options.scope.max_depth = None  # 深度
        self.options.scope.request_methods = [  # 允许的方法
            Request.METHOD_GET,
            Request.METHOD_POST,
            Request.METHOD_PUT,
            Request.METHOD_DELETE,
            Request.METHOD_OPTIONS,
            Request.METHOD_HEAD
        ]

    def _setIdentityOptions(self):
        '''
        设置认证
        refs: 
        '''
        self.options.identity.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})

    def _setIgnoredExtensions(self):
        '''
        设置排除的拓展名
        '''
        self.ignored_extensions = IGNORED_EXTESIONS

    def _setFocusExtensions(self):
        '''
        设置需要的拓展名 
        '''
        self.focus_extensions = []
        self.focus_extensions.extend(EXCEL_EXTENSIONS)
        self.focus_extensions.extend(PDF_EXTENSIONS)
        self.focus_extensions.extend(WORD_EXTENSIONS)
        print(self.focus_extensions)

    def _set_cb_crawler_before_start(self):
        global subdomain_url
        subdomain_url = self.subdomain_url

        def cb_crawler_before_start():
            print("\nTarget : " + subdomain_url)
            print("--" * 30)

        self.options.callbacks.crawler_before_start = cb_crawler_before_start  # Called before the crawler starts crawling. Default is a null route.

    def _set_cb_crawler_after_finish(self):
        def cb_crawler_after_finish(queue):
            print("Crawling finished.")

        self.options.callbacks.crawler_after_finish = cb_crawler_after_finish  # Called after the crawler finished crawling. Default is a null route.

    def _set_cb_request_before_start(self):
        global ignored_extensions, crawled_urls_to_check_dups
        crawled_urls_to_check_dups = self.crawled_urls_to_check_dups
        ignored_extensions = self.ignored_extensions

        def cb_request_before_start(queue, queue_item):
            if queue_item.request.url in crawled_urls_to_check_dups:  # To avoid duplicate links crawling
                return CrawlerActions.DO_SKIP_TO_NEXT
            if extension(queue_item.request.url) in ignored_extensions:  # Don't crawl gif, jpg , etc
                return CrawlerActions.DO_SKIP_TO_NEXT
            return CrawlerActions.DO_CONTINUE_CRAWLING

        self.options.callbacks.request_before_start = cb_request_before_start  # Called before the crawler starts a new request. Default is a null route.

    def _set_cb_request_after_finish(self):
        global crawled_urls_to_check_dups, file_links
        focus_extensions = self.focus_extensions
        crawled_urls_to_check_dups = self.crawled_urls_to_check_dups
        file_links = self.file_links
        result_path = self.reuslt_path
        other_links = self.other_links

        def cb_request_after_finish(queue, queue_item, new_queue_items):
            crawled_urls_to_check_dups.append(queue_item.request.url)  # Add newly obtained URL in list
            # print('-----------')
            # print(crawled_urls_to_check_dups)
            # print('-----------')
            if extension(queue_item.request.url).lower() in focus_extensions:
                path = queue_item.request.url
                file_links.append(path)
                open(result_path + "/" + "file_links.json", "w").write(str(json.dumps(file_links)))
                print(" File > {}".format(queue_item.request.url))

            else:
                if ("?" in queue_item.request.url):
                    path = queue_item.request.url[:queue_item.request.url.find("?")]
                    query = queue_item.request.url[queue_item.request.url.find("?"):]
                else:
                    path = queue_item.request.url
                    query = ""
                other_links[path].append(query)

                open(result_path + "/" + "others_links.json", "w").write(str(json.dumps(other_links)))
                print(" Others> {}".format(queue_item.request.url))

            return CrawlerActions.DO_CONTINUE_CRAWLING

        self.options.callbacks.request_after_finish = cb_request_after_finish  # Called after the crawler finishes a request. Default is a null route.

    def startCrawl(self):
        self._set_cb_crawler_before_start()
        self._set_cb_crawler_after_finish()
        self._set_cb_request_before_start()
        self._set_cb_request_after_finish()

        self.crawler = Crawler(self.options)
        self.crawler.start_with(Request(self.subdomain_url))


if __name__ == '__main__':
    subdomain = "stlhh.zt.ccut.edu.cn"
    links_crawler = LinksCrawler(subdomain)
    links_crawler.prepare()
    links_crawler.setOptions()
    links_crawler.startCrawl()
