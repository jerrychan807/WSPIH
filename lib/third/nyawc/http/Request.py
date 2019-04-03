# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Tijme Gommers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lib.third.nyawc.helpers.URLHelper import URLHelper

class Request(object):
    """The Request class contains details that were used to request the specified URL.

    Attributes:
        METHOD_OPTIONS (str): A request method that can be used to request the URL.
        METHOD_GET (str): A request method that can be used to request the URL.
        METHOD_HEAD (str): A request method that can be used to request the URL.
        METHOD_POST (str): A request method that can be used to request the URL.
        METHOD_PUT (str): A request method that can be used to request the URL.
        METHOD_DELETE (str): A request method that can be used to request the URL.
        parent_raised_error (bool): If the parent request raised an error (e.g. 404).
        depth (int): The current crawling depth.
        url (str): The absolute URL to use when making the request.
        method (str): The request method to use for the request.
        data (obj): The post data {key: value} OrderedDict that will be sent.
        auth (obj): The (requests module) authentication class to use for the request.
        cookies (obj): The (requests module) cookie jar to use for the request.
        headers (obj): The headers {key: value} to use for the request.
        proxies (obj): The proxies {key: value} to use for the request.
        timeout (int): The amount of seconds to wait before a timeout exception will be thrown.
        verify (mixed): True or False based on if certificates should be checked or else a path to a trusted bundle.

    """

    METHOD_OPTIONS = "options"

    METHOD_GET = "get"

    METHOD_HEAD = "head"

    METHOD_POST = "post"

    METHOD_PUT = "put"

    METHOD_DELETE = "delete"

    def __init__(self, url, method=METHOD_GET, data=None, auth=None, cookies=None, headers=None, proxies=None, timeout=30, verify=True):
        """Constructs a Request instance.

        Args:
            url (str): The absolute URL to use when making the request.
            method (str): The request method to use for the request.
            data (obj): The post data {key: value} OrderedDict that will be sent.
            auth (obj): The (requests module) authentication class to use for the request.
            cookies (obj): The (requests module) cookie jar to use for the request.
            headers (obj): The headers {key: value} to use for the request.
            proxies (obj): The proxies {key: value} to use for the request.
            timeout (int): The amount of seconds to wait before a timeout exception will be thrown.
            verify (mixed): True or False based on if certificates should be checked or else a path to a trusted bundle.

        """

        self.parent_raised_error = False
        self.depth = 0

        self.url = url
        self.method = method
        self.auth = auth
        self.cookies = cookies
        self.headers = headers
        self.proxies = proxies
        self.timeout = timeout
        self.verify = verify

        if method == self.METHOD_GET:
            self.url = URLHelper.append_with_data(self.url, data)
            self.data = None
        else:
            self.data = data
