#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/22 11:52 PM
# @Author  : Jerry
# @Desc    : 汇集所有有敏感的结果
# @File    : CombineResult.py



import os
import sys
import json


def combineReuslt(folder_name):
    cmd = "find {0}/* -name 'result.json'".format(folder_name)
    output = os.popen(cmd)

    output_str = output.read()
    result_json_list = output_str.strip().split('\n')
    print(result_json_list)

    all_result_dict = {}
    for each_result in result_json_list:
        print('[*] reading {0}'.format(each_result))

        with open(each_result, 'r') as f:
            temp_result_dict = json.load(f)
            all_result_dict.update(temp_result_dict)

    # print(all_result_dict)

    # 写入all_result.txt文件
    with open("all_result.txt", 'w') as f:
        f.write("vulnerable url num is {0}\n".format(len(all_result_dict)))
        f.write("-------------------\n")
        for url, value_list in all_result_dict.items():
            f.write("url: {}\n".format(url))
            if value_list['phone']:
                f.write("phone evidence: {}\n".format(",".join(value_list['phone'])))
            if value_list['idcard']:
                f.write("idcard evidence: {}\n".format(",".join(value_list['idcard'])))
            if value_list['email']:
                f.write("email evidence: {}\n".format(",".join(value_list['email'])))
            f.write("-------------------\n")


if __name__ == '__main__':
    # folder_name = sys.argv[1]
    folder_name = 'result'
    combineReuslt(folder_name)
