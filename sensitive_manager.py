# -*- coding:utf-8 -*-
__author__ = 'jerry'

import subprocess
import sys
import json
import os

from lib.logger import logger as my_logger


def crawl_xls_links(subdoamin, current_path):
    cmd = 'python3 ' + '/okscan/sensitive_file/xls_links_crawler.py {0} {1}'.format(subdoamin, current_path)
    print cmd
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdoutput, erroutput) = p.communicate()
    except:
        stdoutput = "error"
        err = "There was an exception in  "
        err += function.__name__
        my_logger.exception(err)
    return stdoutput


def create_xls_target_txt(domain_path):
    domain = domain_path.split('/')[-1]
    file_name = domain_path + '/' + '{0}_excel_links.json'.format(domain)
    target_filename = domain_path + '/' + '{0}_target.txt'.format(domain)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            links = json.load(f)

        with open(target_filename, 'a+') as f:
            for k, v in links.items():
                f.write(k + '\n')
        return target_filename
    else:
        return None


def check_sensitive_file(target_txt):
    cmd = 'python ' + '/okscan/sensitive_file/xls_sensitive_parser.py {0}'.format(target_txt)
    print cmd
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdoutput, erroutput) = p.communicate()
    except:
        stdoutput = "error"
        err = "There was an exception in  "
        err += function.__name__
        my_logger.exception(err)
    return stdoutput


def get_subdomain_list(subdomain_file):
    with open(subdomain_file, 'r') as f:
        subdomain_list = [subdomain.strip() for subdomain in f]
    return subdomain_list


def get_domain_name(subdomain):
    subdomain = 'http://' + subdomain if 'http' not in subdomain else subdomain
    domain = subdomain[subdomain.find("://") + 3:]

    if "/" in domain:  # when whole path is specified
        domain = domain[:domain.find("/")]
    return domain


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    subdomain_file = sys.argv[1]
    project_name = sys.argv[2]
    subdomain_list = get_subdomain_list(subdomain_file)
    current_path = os.getcwd()
    print 'current_path: {0}'.format(current_path)
    project_path = os.path.join(current_path, project_name)
    for subdomain in subdomain_list:
        domain_name = get_domain_name(subdomain)

        domain_path = os.path.join(project_path, domain_name)
        print 'domain_path: {0}'.format(domain_path)
        makedir(domain_path)  # create path folder
        crawl_xls_links(subdomain, domain_path)  # crawl xls links ,save in a json file

        target_txt = create_xls_target_txt(domain_path)  # save xls links in target.txt
        if target_txt:
            print 'target_txt: {0}'.format(target_txt)
            check_sensitive_file(target_txt)


if __name__ == '__main__':
    main()
