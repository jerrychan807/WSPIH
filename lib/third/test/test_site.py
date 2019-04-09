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

import os
import unittest

from nyawc.Options import Options
from nyawc.Crawler import Crawler
from nyawc.http.Request import Request
from nyawc.CrawlerActions import CrawlerActions

class TestSite(unittest.TestCase):
    """The TestSite class checks if the crawler handles invalid responses correctly.

    Attributes:
        travis (bool): If the current environment is in Travis CI.

    """

    def __init__(self, *args, **kwargs):
        """Initialize the unit test and mark if the current environment is Travis CI.

        Args:
            args list(str): The command line arguments.
            kwargs **: Extra arguments

        """

        super(TestSite, self).__init__(*args, **kwargs)
        self.travis = "UNITTEST_NYAWC_SITE" in os.environ

    def cb_request_after_finish(self, queue, queue_item, new_queue_items):
        """Crawler callback for when a request is finished crawling.

        Args:
            queue (:class:`nyawc.Queue`): The current crawling queue.
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            new_queue_items list(:class:`nyawc.QueueItem`): The new queue items that were found in the one that finished.

        Returns:
            str: A crawler action (either DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        print("Finished: {}".format(queue_item.request.url))
        return CrawlerActions.DO_CONTINUE_CRAWLING

    def test_crawl_website(self):
        """Crawl the website in `test/` and check if the count is correct."""

        if not self.travis:
            print("\n\nPlease note that the 'TestSite' unit test did not run.")
            print("It will only run in Travis CI since it requires a webserver.\n")
            return

        options = Options()
        options.callbacks.request_after_finish = self.cb_request_after_finish
        crawler = Crawler(options)
        crawler.start_with(Request("http://localhost/"))

        self.assertEqual(crawler.queue.count_total, 18)
