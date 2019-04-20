# !/usr/local/bin/python3
# -*- coding:utf-8 -*-


with open('target/src.txt','r') as f:
    new_list = ["http://{0}".format(line) for line in f]

with open('target/http_src.txt','w') as f1:
    for i in new_list:
        f1.write("{}".format(i))
