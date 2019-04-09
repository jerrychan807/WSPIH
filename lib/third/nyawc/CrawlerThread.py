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

import threading

from lib.third.nyawc.helpers.DebugHelper import DebugHelper
from lib.third.nyawc.http.Handler import Handler
from lib.third.nyawc.QueueItem import QueueItem

class CrawlerThread(threading.Thread):
    """The crawler thread executes the HTTP request using the HTTP handler.

    Attributes:
        __callback (obj): The method to call when finished
        __callback_lock (bool): The callback lock that prevents race conditions.
        __options (:class:`nyawc.Options`): The settins/options object.
        __queue_item (:class:`nyawc.QueueItem`): The queue item containing a request to execute.

    """

    def __init__(self, callback, callback_lock, options, queue_item):
        """Constructs a crawler thread instance

        Args:
            callback (obj): The method to call when finished
            callback_lock (bool): The callback lock that prevents race conditions.
            options (:class:`nyawc.Options`): The settins/options object.
            queue_item (:class:`nyawc.QueueItem`): The queue item containing a request to execute.

        """

        threading.Thread.__init__(self)

        self.__callback = callback
        self.__callback_lock = callback_lock
        self.__options = options
        self.__queue_item = queue_item

    def run(self):
        """Executes the HTTP call.

        Note:
            If this and the parent handler raised an error, the queue item status
            will be set to errored instead of finished. This is to prevent e.g. 404
            recursion.

        """

        try:
            self.__options.callbacks.request_in_thread_before_start(self.__queue_item)
        except Exception as e:
            print(e)

        new_requests = []
        failed = False

        try:
            handler = Handler(self.__options, self.__queue_item)
            new_requests = handler.get_new_requests() # 解析页面获取新的请求
            print(new_requests)
            print('---------new_requests------------')
            try:
                self.__queue_item.response.raise_for_status()
            except Exception:
                if self.__queue_item.request.parent_raised_error:
                    failed = True
                else:
                    for new_request in new_requests:
                        new_request.parent_raised_error = True

        except Exception as e:
            failed = True

            error_message = "Setting status of '{}' to '{}' because of an HTTP error.".format(
                self.__queue_item.request.url,
                QueueItem.STATUS_ERRORED
            )

            DebugHelper.output(self.__options, error_message)
            DebugHelper.output(self.__options, e)

            try:
                self.__options.callbacks.request_on_error(self.__queue_item, str(e))
            except Exception as e:
                print(e)

        for new_request in new_requests:
            new_request.parent_url = self.__queue_item.request.url

        try:
            self.__options.callbacks.request_in_thread_after_finish(self.__queue_item)
        except Exception as e:
            print(e)

        with self.__callback_lock:
            self.__callback(self.__queue_item, new_requests, failed)
