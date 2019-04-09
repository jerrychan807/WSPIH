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

from nyawc.helpers.URLHelper import URLHelper

class TestUrlHelper(unittest.TestCase):
    """The TestUrlHelper class checks if the methods in the URLHelper work correctly."""

    def test_make_absolute(self):
        """Check if the make absolute method works correctly."""

        host = "https://example.ltd/current"

        tests = [
            ("https://example.ltd/new.html", "new.html"),
            ("https://example.ltd/new", "new"),
            ("https://example.ltd/new1/new2", "new1/new2"),
            ("https://example.ltd/new1/new3", "/new1/new3"),
            ("https://example.ltd/current?a=a", "?a=a")
        ]

        for test in tests:
            self.assertEqual(URLHelper.make_absolute(host, test[1]), test[0])

    def test_make_absolute_with_base(self):
        """Check if the make absolute method works correctly in interpreted with a base URL."""

        host = "https://example.ltd/base/"

        tests = [
            ("https://example.ltd/base/new.html", "new.html"),
            ("https://example.ltd/base/new", "new"),
            ("https://example.ltd/base/new1/new2", "new1/new2"),
            ("https://example.ltd/new1/new2", "/new1/new2"),
            ("https://example.ltd/base/?a=a", "?a=a")
        ]

        for test in tests:
            self.assertEqual(URLHelper.make_absolute(host, test[1]), test[0])

    def test_make_absolute_folder_traversal(self):
        """Ensure folder traversal works correclty."""

        host = "https://example.ltd/dir1/dir2/dir3"

        tests = [
            ("https://example.ltd/dir1/dir2", "../"),
            ("https://example.ltd/dir1", "../../"),
            ("https://example.ltd", "../../../"),
            ("https://example.ltd", "../../../../"),
            ("https://example.ltd", "../../../../../")
        ]

        for test in tests:
            self.assertEqual(URLHelper.make_absolute(host, test[1]), test[0])

    def test_get_protocol(self):
        """Check if the get protocol method works correctly."""

        tests = [
            ("", "domain.tld"),
            ("http", "http://domain.tld"),
            ("arbitrary", "arbitrary://omain.tld")
        ]

        for test in tests:
            self.assertEqual(URLHelper.get_protocol(test[1]), test[0])

    def test_get_subdomain(self):
        """Check if the get subdomain method works correctly."""

        tests = [
            ("", ""),
            ("", "http://"),
            ("", "http://domain"),
            ("", "http://domain.tld"),
            ("sub1", "http://sub1.domain.tld"),
            ("sub2.sub1", "http://sub2.sub1.domain.tld"),
            ("sub3.sub2.sub1", "http://sub3.sub2.sub1.domain.tld")
        ]

        for test in tests:
            self.assertEqual(URLHelper.get_subdomain(test[1]), test[0])

    def test_get_hostname(self):
        """Check if the get hostname method works correctly."""

        tests = [
            ("", ""),
            ("", "http://"),
            ("domain", "http://domain"),
            ("domain", "http://domain.tld"),
            ("domain", "http://sub1.domain.tld"),
            ("domain", "http://sub2.sub1.domain.tld")
        ]

        for test in tests:
            self.assertEqual(URLHelper.get_hostname(test[1]), test[0])

    def test_get_tld(self):
        """Check if the get tld method works correctly."""

        tests = [
            ("", ""),
            ("", "http://"),
            ("", "http://domain"),
            ("tld", "http://domain.tld"),
            ("tld", "http://sub1.domain.tld"),
            ("tld", "http://sub2.sub1.domain.tld")
        ]

        for test in tests:
            self.assertEqual(URLHelper.get_tld(test[1]), test[0])

    def test_get_ordered_params(self):
        """Check if the get ordered params method works correctly."""

        val1 = URLHelper.get_ordered_params("http://example.tld?a=a&c=c&b=b&d=d")
        val2 = URLHelper.get_ordered_params("http://sub.domain.ltd?c=c&b=b&a=a&d=d")

        self.assertEqual(val1, val2)

    def test_append_with_data_encoded_and_decoded(self):
        """Make sure values do not get decoded or encoded."""

        val1 = URLHelper.append_with_data("http://example.tld/", {"val": "{{aaaa}}"})
        val2 = URLHelper.append_with_data("http://example.tld/", {"val": "%7B%7Baaaa%7D%7D"})

        self.assertEqual(val1, "http://example.tld/?val={{aaaa}}")
        self.assertEqual(val2, "http://example.tld/?val=%7B%7Baaaa%7D%7D")
