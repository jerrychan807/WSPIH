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

from lib.third.nyawc.scrapers.HTMLSoupLinkScraper import HTMLSoupLinkScraper
from lib.third.nyawc.QueueItem import QueueItem
from lib.third.nyawc.http.Request import Request
from lib.third.nyawc.http.Response import Response
from lib.third.nyawc.Options import Options

class TestScrapersHTMLSoupLinkScraper(unittest.TestCase):
    """The TestScrapersHTMLSoupLinkScraper class tests if the HTMLSoupLinkScraper is working correctly.

    Attributes:
        __host (str): The host were the new URLs were found on
        __urls list(obj): The URLs that were found

    Note:
        URL 12 (?unique=12) is a unicode type since it contains UTF-8 characters. The `requests`
        library does encode/decode response bodies causing the test to fail if it's an UTF-8 string.

    """

    __host = "https://example.ltd/"

    __urls = [
        {"url": """https://example.ltd?unique=1""", "must_pass": True, "test": """<a href="https://example.ltd?unique=1">test</a>"""},
        {"url": """https://example.ltd/?unique=2""", "must_pass": True, "test": """<a href="https://example.ltd/?unique=2">test</a>"""},
        {"url": """http://example.ltd?unique=3""", "must_pass": True, "test": """<a href="http://example.ltd?unique=3">test</a>"""},
        {"url": """http://example.ltd/?unique=4""", "must_pass": True, "test": """<a href="http://example.ltd/?unique=4">test</a>"""},
        {"url": """https://example.ltd?unique=5""", "must_pass": True, "test": """<a href="//example.ltd?unique=5">test</a>"""},
        {"url": """https://example.ltd/?unique=6""", "must_pass": True, "test": """<a href="//example.ltd/?unique=6">test</a>"""},
        {"url": """https://example.ltd/?unique=7""", "must_pass": True, "test": """<a a="b" c=d href="//example.ltd/?unique=7">test</a>"""},
        {"url": """https://example.ltd/?unique=8""", "must_pass": True, "test": """<a href="//example.ltd/?unique=8" a=b c="d">test</a>"""},
        {"url": """https://example.ltd/?unique=9""", "must_pass": True, "test": """<a a="b" c=d href="//example.ltd/?unique=9" a=b c="d">test</a>"""},
        {"url": """https://example.ltd/index.php?unique=10""", "must_pass": True, "test": """<a href="https://example.ltd/index.php?unique=10">test</a>"""},
        {"url": """https://example.ltd/index.php?unique=11&d=c""", "must_pass": True, "test": """<a href="https://example.ltd/index.php?unique=11&d=c">test</a>"""},
        {"url": u"""https://example.ltd/index.php?unique=12&utf8=\u2713""", "must_pass": True, "test": u"""<a href="https://example.ltd/index.php?unique=12&utf8=\u2713">test</a>"""},
        {"url": """https://example.ltd/index.php?unique=13""", "must_pass": True, "test": """<a href="https://example.ltd/index.php?unique=13#anchor">test</a>"""},
        {"url": """https://example.ltd/folder1/folder2/folder3?unique=14""", "must_pass": True, "test": """<a href="https://example.ltd/folder1/folder2/folder3?unique=14">test</a>"""},
        {"url": """https://example.ltd/folder1/../folder2/folder3?unique=15""", "must_pass": True, "test": """<a href="https://example.ltd/folder1/../folder2/folder3?unique=15">test</a>"""},
        {"url": """https://example.ltd/../folder1/folder2/folder3?unique=16""", "must_pass": True, "test": """<a href="https://example.ltd/../folder1/folder2/folder3?unique=16">test</a>"""},
        {"url": """https://example.ltd/folder1/folder2/folder3?unique=17""", "must_pass": True, "test": """<a href="/folder1/folder2/folder3?unique=17">test</a>"""},
        {"url": """https://example.ltd/folder1/folder2/folder3?unique=18""", "must_pass": True, "test": """<a href="../folder1/folder2/folder3?unique=18">test</a>"""},
        {"url": """https://example.ltd/folder1/folder2/folder3?unique=19""", "must_pass": True, "test": """<a href="../../folder1/folder2/folder3?unique=19">test</a>"""},
        {"url": """https://example.ltd/folder1/folder2/folder3?unique=20""", "must_pass": True, "test": """<a href="/../../folder1/folder2/folder3?unique=20">test</a>"""},
        {"url": """https://example.ltd/?unique=21""", "must_pass": True, "test": """<a href='https://example.ltd/?unique=21'>test</a>"""},
        {"url": """https://example.ltd/?unique=22""", "must_pass": True, "test": """<a href=`https://example.ltd/?unique=22`>test</a>"""},
        {"url": """https://example.ltd/unique=23/folder'/?unique=23""", "must_pass": True, "test": """<a href=`https://example.ltd/unique=23/folder'/?unique=23`>test</a>"""},
        {"url": """https://example.ltd/unique=24/folder"/?unique=24""", "must_pass": True, "test": """<a href=`https://example.ltd/unique=24/folder"/?unique=24`>test</a>"""},
        {"url": """https://example.ltd/unique=25/folder'/?unique=25""", "must_pass": True, "test": """<a href="https://example.ltd/unique=25/folder'/?unique=25">test</a>"""},
        {"url": """https://example.ltd/unique=26/folder`/?unique=26""", "must_pass": True, "test": """<a href="https://example.ltd/unique=26/folder`/?unique=26">test</a>"""},
        {"url": """https://example.ltd/unique=27/folder"/?unique=27""", "must_pass": True, "test": """<a href='https://example.ltd/unique=27/folder"/?unique=27'>test</a>"""},
        {"url": """https://example.ltd/unique=28/folder`/?unique=28""", "must_pass": True, "test": """<a href='https://example.ltd/unique=28/folder`/?unique=28'>test</a>"""},
        {"url": """https://example.ltd/unique=29/folder`/?unique=29""", "must_pass": True, "test": """<a href='https://example.ltd/unique=29/folder`/?unique=29'&b=not-included'>test</a>"""},
        {"url": """https://example.ltd/unique=30/folder`/?unique=30'&b=included""", "must_pass": True, "test": """<a href="https://example.ltd/unique=30/folder`/?unique=30'&b=included">test</a>"""},
        {"url": """https://example.ltd/sample/page/1?unique=31""", "must_pass": True, "test": """<a href="sample/page/1?unique=31">test</a>"""},
        {"url": """https://example.ltd/page/2?unique=32""", "must_pass": True, "test": """<a href="/page/2?unique=32">test</a>"""},
        {"url": """https://example.ltd/page/3?unique=33""", "must_pass": True, "test": """<a href="page/3?unique=33">test</a>"""},
        {"url": """https://example.ltd/page4?unique=34""", "must_pass": True, "test": """<a href="page4?unique=34">test</a>"""},
        {"url": """http://examp%0ale.ltd/?unique=35""", "must_pass": True, "test": """<a href="http://examp%0ale.ltd/?unique=35">"""},
        {"url": """http://examp\nle.ltd/?unique=36""", "must_pass": True, "test": """<a href="http://examp\nle.ltd/?unique=36">"""}
    ]

    def test_soup_url_count(self):
        """Test if the amount of URLs found complies with the expected amount."""

        html = ""
        for url in self.__urls:
            html += "\n" + url["test"]

        request = Request(self.__host)
        response = Response(self.__host)
        response.text = html

        finder = HTMLSoupLinkScraper(Options(), QueueItem(request, response))
        matches = finder.get_requests()

        self.assertEqual(len(matches), 36)

    def test_soup_url_matches(self):
        """Test if all the URLs match the found URLs."""

        for url in self.__urls:
            request = Request(self.__host)
            response = Response(self.__host)
            response.text = url["test"]

            finder = HTMLSoupLinkScraper(Options(), QueueItem(request, response))
            requests = finder.get_requests()

            if url["must_pass"]:
                self.assertEqual(requests[0].url, url["url"])
                self.assertEqual(len(requests), 1)
            else:
                self.assertEqual(len(requests), 0)


if __name__ == '__main__':
    unittest.main()