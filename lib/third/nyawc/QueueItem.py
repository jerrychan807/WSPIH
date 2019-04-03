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
from bs4 import BeautifulSoup

class QueueItem(object):
    """The QueueItem class keeps track of the request and response and the crawling status.

    Attributes:
        STATUS_QUEUED (str): Status for when the crawler did not yet start the request.
        STATUS_IN_PROGRESS (str): Status for when the crawler is currently crawling the request.
        STATUS_FINISHED (str): Status for when the crawler has finished crawling the request.
        STATUS_CANCELLED (str): Status for when the crawler has cancelled the request.
        STATUS_ERRORED (str): Status for when the crawler could not execute the request.
        STATUSES (arr): All statuses.
        status (str): The current crawling status.
        decomposed (bool): If the this queue item is decomposed.
        request (:class:`nyawc.http.Request`): The Request object.
        response (:class:`nyawc.http.Response`): The Response object.
        __response_soup (obj): The BeautifulSoup container for the response text.
        __index_hash (str): The index of the queue (if cached), otherwise None.

    Note:
        A queue item will be decomposed (cached objects are deleted to free up memory) when it is
        not likeley to be used again. After decompisition variables will not be cached anymore.

    """

    STATUS_QUEUED = "queued"

    STATUS_IN_PROGRESS = "in_progress"

    STATUS_FINISHED = "finished"

    STATUS_CANCELLED = "cancelled"

    STATUS_ERRORED = "errored"

    STATUSES = [
        STATUS_QUEUED,
        STATUS_IN_PROGRESS,
        STATUS_FINISHED,
        STATUS_CANCELLED,
        STATUS_ERRORED
    ]

    def __init__(self, request, response):
        """Constructs a QueueItem instance.

        Args:
            request (:class:`nyawc.http.Request`): The Request object.
            response (:class:`nyawc.http.Response`): The Response object (empty object when initialized).

        """

        self.status = QueueItem.STATUS_QUEUED
        self.decomposed = False
        self.__response_soup = None
        self.__index_hash = None

        self.request = request
        self.response = response

    def get_soup_response(self):
        """Get the response as a cached BeautifulSoup container.

        Returns:
            obj: The BeautifulSoup container.

        """

        if self.response is not None:
            if self.__response_soup is None:
                result = BeautifulSoup(self.response.text, "lxml")

                if self.decomposed:
                    return result
                else:
                    self.__response_soup = BeautifulSoup(self.response.text, "lxml")

        return self.__response_soup

    def decompose(self):
        """Decompose this queue item (set cached variables to None) to free up memory.

        Note:
            When setting cached variables to None memory will be released after the garbage 
            collector ran.
        
        """

        self.__response_soup = None

        self.decomposed = True

    def get_hash(self):
        """Generate and return the dict index hash of the given queue item.

        Note:
            Cookies should not be included in the hash calculation because
            otherwise requests are crawled multiple times with e.g. different
            session keys, causing infinite crawling recursion.

        Note:
            At this moment the keys do not actually get hashed since it works perfectly without and
            since hashing the keys requires us to built hash collision management.

        Returns:
            str: The hash of the given queue item.

        """

        if self.__index_hash:
            return self.__index_hash

        key = self.request.method

        key += URLHelper.get_protocol(self.request.url)
        key += URLHelper.get_subdomain(self.request.url)
        key += URLHelper.get_hostname(self.request.url)
        key += URLHelper.get_tld(self.request.url)
        key += URLHelper.get_path(self.request.url)

        key += str(URLHelper.get_ordered_params(self.request.url))

        if self.request.data is not None:
            key += str(self.request.data.keys())

        self.__index_hash = key
        return self.__index_hash
