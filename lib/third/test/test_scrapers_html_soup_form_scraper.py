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

from nyawc.scrapers.HTMLSoupFormScraper import HTMLSoupFormScraper
from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response
from nyawc.Options import Options

class TestScrapersHTMLSoupFormScraper(unittest.TestCase):
    """The TestScrapersHTMLSoupFormScraper class tests if the HTMLSoupFormScraper is working correctly.

    Attributes:
        __host (str): The host were the new URLs were found on
        __urls list(obj): The URLs that were found

    """

    __host = "https://example.ltd/"

    __urls = [
        {
            "url": """https://example.ltd/action_page1.php""",
            "method": Request.METHOD_POST,
            "data": {
                "lastname": "Mouse",
                "name": "TestContent"
            },
            "must_pass": True,
            "test": """
                <form action="/action_page1.php" method="post">
                    First name:<br>
                    <input type="text" value="Mickey"><br>
                    Last name:<br>
                    <input type="text" name="lastname" value="Mouse"><br><br>
                    <input type="submit" value="Submit">
                    <textarea name="test">TestContent</textarea>
                </form>
            """
        },
        {
            "url": """https://example.ltd/action_page2.php""",
            "method": Request.METHOD_POST,
            "data": {
                "lastname": "Mouse"
            },
            "must_pass": True,
            "test": """
                <form action=`/action_page2.php` method="Post">
                    First name:<br>
                    <input type="text" value="Mickey"><br>
                    Last name:<br>
                    <input type="text" name="lastname" value="Mouse"><br><br>
                    <input type="submit" value="Submit">
                </form>
            """
        },
        {
            "url": """https://example.ltd/?lastname=Mouse""",
            "method": Request.METHOD_GET,
            "data": None,
            "must_pass": True,
            "test": """
                <form method="geT">
                    First name:<br>
                    <input type="text" value="Mickey"><br>
                    Last name:<br>
                    <input type="text" name="lastname" value="Mouse"><br><br>
                    <input type="submit" value="Submit">
                </form>
            """
        },
        {
            "url": """https://example.ltd/?lastname=Mouse&test=TestContent""",
            "method": Request.METHOD_GET,
            "data": None,
            "must_pass": True,
            "test": """
                <form>
                    First name:<br>
                    <input type="text" value="Mickey"><br>
                    Last name:<br>
                    <input type="text" name="lastname" value="Mouse"><br><br>
                    <textarea name="test">TestContent</textarea>
                    <input type="submit" value="Submit">
                </form>
            """
        },
    ]

    def test_soup_url_count(self):
        """Test if the amount of URLs found complies with the expected amount."""

        html = ""
        for url in self.__urls:
            html += "\n" + url["test"]

        request = Request(self.__host)
        response = Response(self.__host)
        response.text = html

        finder = HTMLSoupFormScraper(Options(), QueueItem(request, response))
        matches = finder.get_requests()

        self.assertEqual(len(matches), 4)

    def test_soup_url_matches(self):
        """Test if all the URLs match the found URLs."""

        for url in self.__urls:
            request = Request(self.__host)
            response = Response(self.__host)
            response.text = url["test"]

            finder = HTMLSoupFormScraper(Options(), QueueItem(request, response))
            requests = finder.get_requests()

            if url["must_pass"]:
                self.assertEqual(requests[0].url, url["url"])
                self.assertEqual(len(requests), 1)
            else:
                self.assertEqual(len(requests), 0)
