#!/usr/bin/env python
# -*-coding:utf-8 -*-

# @Time    : 2019/3/26 14:23
# @Author  : EXHades
# @Email   : exhades1337@gmail.com

"""
下载 txt 里面的 xls -> 读取 xls 里面的信息 -> 匹配敏感字节 (手机号 / 身份证 / 邮箱) -> 打印出敏感字符与相关链接
"""
import os
import re
import sys
import time
from urllib import unquote  # 只用了解url编码模块
import requests
import xlrd

# 设置系统默认字符编码

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as err:
    print(err)

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
           'referer': 'http://sysu.edu.cn/'}

# 获取当前文件夹
# filepath = sys.argv[0][:-len(sys.argv[0].split('/')[-1])]

# 正则表达式
# 电话号
phone = r'^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$'
# 邮箱
email = r'^\w+@(\w+\.)+\w+$'
# 身份证
id_card = r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'

ph_top_three_list = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153',
                     '154', '155', '156', '157', '158', '159', '180', '181', '182', '183', '184', '185', '186', '187',
                     '188', '189']

demo_list = ['张三', '李四', '王二', 'zhangsan', 'lisi']
# sensitive_list = ['账号', '密码', 'user', 'password']
sensitive_list = []


def read_xls(path_file_name, url, filename, sensitive_list):
    '''
    读取xls,并且匹配敏感字符,处理敏感字符，最后写入文件
    '''

    # print('[*] URL为:{}'.format(url))
    # print('xls文件本地路径为:{}'.format(path_file_name))

    # 打开工作表
    # test_data = xlrd.open_workbook('test.xlsx', encoding_override="urf-8")
    test_data = xlrd.open_workbook(path_file_name)

    # print('[*] 读取 {} 表'.format(filename)).encode('gbk')
    # 获取全部工作表名
    text_data_sheet_name = test_data.sheet_names()
    # print('[*] 表内有 Sheet {} 页，分别为：{}'.format(len(text_data_sheet_name), text_data_sheet_name)).encode('gbk')

    # 匹配到的敏感字符列表
    ph_sensitive = []
    em_sensitive = []
    id_sensitive = []
    up_sensitive = []

    # 按工作表名循环获取数据
    for tables_name in text_data_sheet_name:
        # print('[*] 开始检查【{}】页'.format(tables_name))
        # 通过工作表名选择工作表
        table = test_data.sheet_by_name(tables_name)
        # 工作表行数
        nrows = table.nrows
        # 判断表格是否为空
        if nrows == 0:
            # print('[*] 【{}】工作表为空,跳过'.format(tables_name))
            continue

        # 循环工作表每一行
        for rownum in range(nrows):
            # 循环获取每个单元格的值
            for cell in table.row_values(rownum):
                # 判断单元格是否为空
                if cell != '':
                    # 去掉结尾空格
                    cell = str(cell).strip()
                    # 判断是否存在敏感字节

                    # 匹配敏感字节列表

                    # 单元格内字符串完全匹配敏感字节
                    # if cell in sensitive_list:
                    #     up_sensitive.append(cell)

                    # 单元格内字符串包含敏感字节
                    for sen in sensitive_list:
                        cell = cell.decode('utf-8')
                        value = cell.find(sen)
                        if value != -1:
                            up_sensitive.append(cell)

                    # 匹配敏感字符
                    ph = re.search(phone, cell)
                    em = re.search(email, cell)
                    idcard = re.search(id_card, cell)

                    if ph:
                        ph = ph.group()
                        # 匹配正则到的手机号码前三数字，以确定是否为真正的号码
                        for ph_top_three in ph_top_three_list:
                            if ph[0:3] == ph_top_three:
                                ph_sensitive.append(ph)
                            else:
                                pass
                    elif em:
                        em = em.group()  # 获取正则匹配到的str
                        # 判断正则到的邮箱是否为 demo 邮箱
                        # em的值是字符串 "xxx@xxx.com" 所以使用split 以 "@"符号分割得到一个列表
                        # 然后list[0] 得到@前面的字符串
                        # 直接判断判断@前面的字符串在不在 demo_list 中 如果不在则写入
                        if em.split('@')[0] not in demo_list:
                            em_sensitive.append(em)

                    elif idcard:
                        id_sensitive.append(idcard.group())
                    else:
                        pass
                else:
                    pass

    # 分别去重 3 个敏感字符列表
    ph_sensitive = list(set(ph_sensitive))
    em_sensitive = list(set(em_sensitive))
    id_sensitive = list(set(id_sensitive))
    up_sensitive = list(set(up_sensitive))

    # 判断各敏感字节列表中元素长度
    # 去重后整个列表还只要一个元素，一般就是示例,直接清空 list
    if len(ph_sensitive) == 1:
        ph_sensitive = []
    if len(em_sensitive) == 1:
        em_sensitive = []
    if len(id_sensitive) == 1:
        id_sensitive = []

    # 汇总敏感字符列表
    sensitive = up_sensitive + ph_sensitive + em_sensitive + id_sensitive

    # 判断汇总的敏感字符列表是否为空
    # 一个空 list 本身等同于 False
    global filepath
    if sensitive:
        sensitive_str = ','.join(sensitive)
        ok_list = open(filepath + 'result.txt', 'a')
        ok_list.write(
            """[!] URL: {}\n[!] 文件名: {}\n[!] 敏感字符: {}\n[*]{}\n""".format(url, filename, sensitive_str.decode('utf-8'),
                                                                         ('-' * 60)))
        ok_list.close()
        print(
            """[!] URL: {}\n[!] 文件名: {}\n[!] 敏感字符: {}\n[*]{}\n""".format(url, filename, sensitive_str.decode('utf-8'),
                                                                         ('-' * 60)))
    else:
        print('[*] 该表格并无敏感数据！')


# 成功下载文件的次数
number = 0


def download_xls(txt_path, sensitive_list):
    '''
    读 txt 里链接下载 xls 保存本地文件夹，然后调用 readxls 匹配敏感字符
    '''

    global number
    global filepath
    # 用 / 分隔 txt_path 取最后的文件名 然后判断长度 在用 [:-长度]取出路径
    filepath = txt_path[:-len(txt_path.split('/')[-1])]
    # if os.path.isdir('xls_list'):
    #     print('[*] xls_list 目录已存在,路径为{}/xls_list'.format(filepath)).encode('gbk')
    #     print('-' * 60)
    # else:
    #     print('[*] 创建 xls_list 目，用于存在 xls 文件,路径为{}/xls_list'.format(filepath)).encode('gbk')
    #     print('-' * 60)

    # filepath 结尾存在/
    xls_list_path = filepath + 'xls_list'
    try:
        os.mkdir(xls_list_path)
        print('[*] xls_list 目，用于存在 xls 文件,路径为{}'.format(xls_list_path))
    except Exception as err:
        pass

    print('[!] 开始下载 xls 并开始匹配敏感字符')
    try:
        # 循环列表下载 xls 保存到 xls_list 表格
        xls_list = open(txt_path)
        for xls_url in xls_list.readlines():
            # 去掉末尾的 \ n 换行符
            url = xls_url.strip('\n')
            # 处理文件名与保存路径
            url_name = url.split("/")  # url 字符串按/分割
            # 读取文件名字符串，并解码url编码为中文
            get_name = str(unquote(str(url_name[-1:])))
            # 从 list 中提取出文件名 例如：['广东省博士后工作站联系表.xls'] 提取为 广东省博士后工作站联系表.xls
            filename = get_name[2:-2]
            # 文件保存完整路径
            path_file_name = xls_list_path.decode('utf-8') + '/' + filename
            if os.path.exists(path_file_name):
                continue
            try:
                # 下载文件保存到 xls_list 表格
                r = requests.get(url, headers=headers)
                # 判断http状态
                if r.status_code == 200:
                    with open(path_file_name.decode('utf-8'), "wb") as xls_file:
                        xls_file.write(r.content)
                        print('[*] {} 下载文件:【{}】,并开始检测敏感字符'.format(
                            time.strftime("%Y%m%d-%H:%M:%S", time.localtime(time.time())), filename))
                        number += 1
                    # 读取xls并且匹配敏感字节
                    read_xls(path_file_name, url, filename, sensitive_list)
                else:
                    print('URL状态码为:{}的URL:{}'.format(str(r.status_code()), url)).encode('gbk')
                    # err_list = open('err_list.txt', 'a')
                    # err_list.write('状态码为:{}的URL:{}'.format(str(r.status_code()), url))
                    # err_list.close()

            except Exception as err:
                # '''报错URL'''
                err_list = open('err_list.txt', 'a')
                err_list.write('URL:【{}】报错{}\n'.format(url, err))
                err_list.close()
                # print(url)
                # print(err)
                # err_url = open('err_url.txt', 'a')
                # err_url.write('{}\n'.format(url))
                # err_url.close()
                pass
    except Exception as err:
        pass


def load_sensitive_list(sensitive_list_path):
    f = open(sensitive_list_path, 'r')
    sourceInLine = f.readlines()
    print sourceInLine
    dataset = []
    for line in sourceInLine:
        temp1 = line.split(',')
        for i in temp1:
            if i:
                dataset.append(i)
    return dataset


def run(txt_path):
    global sensitive_list
    sensitive_list_path = './sensitive.txt'
    sensitive_list = load_sensitive_list(sensitive_list_path)
    print ('[*]' + '-' * 59)
    print('[*] 敏感字节列表:')
    for sensitive in sensitive_list:
        print sensitive
    print('*' * 60)
    print('[*] {} Runing'.format(time.strftime("%Y%m%d-%H:%M:%S", time.localtime(time.time()))))
    download_xls(txt_path, sensitive_list)
    print('[*]' + '-' * 59)
    print('[!] 检测结果保存在:【{}】'.format('result.txt'))
    # print('[!] 存在错误的URL&文件报错信息分别存放在【{}】与【{}】'.format((filepath + 'err_url.txt'), (filepath + 'err_list.txt')))
    print('[!] {} 完成匹配任务共成功检测了{}个文件'.format(time.strftime("%Y%m%d-%H:%M:%S", time.localtime(time.time())),
                                            number))
    print('[*]' + '-' * 59)


if __name__ == "__main__":
    txt_path = sys.argv[1]
    run(txt_path)
