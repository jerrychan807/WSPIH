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

import unittest

from nyawc.helpers.HTTPRequestHelper import HTTPRequestHelper
from nyawc.Queue import Queue
from nyawc.http.Request import Request
from nyawc.Options import Options

class TestQueue(unittest.TestCase):
    """The TestQueue class tests if the hashes and counters of the queue work correctly."""

    def test_hash_is_always_the_same(self):
        """Ensure the hashes are calculated correctly by checking for duplicates in the queue."""

        options = Options()
        queue = Queue(options)

        for index in range(0, 100):
            request = Request("https://example.ltd?1=1#2=2")
            HTTPRequestHelper.patch_with_options(request, options)
            request.cookies.set(name='tasty_cookie{}'.format(index), value='yum', domain='example.ltd')
            queue.add_request(request)

        self.assertEqual(queue.count_total, 1)

    def test_hash_different_query_order(self):
        """Ensure query parameters in different orders are treated as one queue item."""

        queue = Queue(Options())

        queue.add_request(Request("https://www.example.ltd?b=b&c=c&a=a"))
        queue.add_request(Request("https://www.example.ltd?b=b&a=a&c=c"))
        queue.add_request(Request("https://www.example.ltd?a=a&b=b&c=c"))

        self.assertEqual(queue.count_total, 1)


    def test_hash_different_encoded_and_decoded_values(self):
        """Ensure encoded and decoded values have a different hash."""

        queue = Queue(Options())

        queue.add_request(Request("http://example.ltd?val={{aaaa}}"))
        queue.add_request(Request("http://example.ltd?val=%7B%7Baaaa%7D%7D"))

        self.assertEqual(queue.count_total, 2)
