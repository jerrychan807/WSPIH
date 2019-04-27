#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/27 5:00 PM
# @Author  : Jerry
# @Desc    : 
# @File    : config.py

# 爬取网站超时时间,单位为s
CRAWLER_SITE_TIMEOUT = 1200

# 爬虫深度
CRAWLER_MAX_DEPTH = 15

# 爬虫线程数
CRAWLER_MAX_THREADS = 20

# 爬虫请求页面超时时间,单位为s
CRAWLER_REQUEST_TIMEOUT = 30

# 下载文件并发数
DOWNLOAD_WORKER_NUM = 10

# 下载文件超时时间,单位为s
DOWNLOAD_TIMEOUT = 20
