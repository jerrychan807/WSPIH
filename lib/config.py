#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/15 12:16 AM
# @Author  : Jerry
# @Desc    : 
# @File    : config.py


from lib.common.logger import Logger
from lib.common.basic import getCurrentPath

import os

project_path = getCurrentPath()
log = Logger(os.path.join(project_path, 'error.log')
             , level='debug')
