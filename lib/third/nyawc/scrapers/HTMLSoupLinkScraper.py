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

from nyawc.http.Request import Request
from nyawc.helpers.URLHelper import URLHelper
from nyawc.scrapers.BaseScraper import BaseScraper

class HTMLSoupLinkScraper(BaseScraper):
    """The HTMLSoupLinkScraper finds URLs from href attributes in HTML using BeautifulSoup.

    Attributes:
        content_types list(str): The supported content types.

    """

    content_types = [
        "text/html",
        "application/xhtml+xml"
    ]

    def derived_get_requests(self):
        """Get all the new requests that were found in the response.

        Returns:
            list(:class:`nyawc.http.Request`): A list of new requests that were found.

        """

        attributes = {
            "src": True,
            "href": True,
            "link": True,
            "script": True,
            "url": True
        }

        host = self.queue_item.response.url
        soup = self.queue_item.get_soup_response()
        base_element = soup.find("base", href=True)
        elements = soup.select("[{}]".format("],[".join(attributes.keys())))

        # Always use the URL from the base element if it exists.
        # https://www.w3schools.com/tags/tag_base.asp
        if base_element:
            host = URLHelper.make_absolute(host, base_element["href"])

        found_requests = []

        for element in elements:
            for attribute in attributes.keys():
                if not element.has_attr(attribute):
                    continue

                found_url = self.__trim_grave_accent(element[attribute])

                if URLHelper.is_mailto(found_url):
                    continue

                absolute_url = URLHelper.make_absolute(host, found_url)
                found_requests.append(Request(absolute_url))

        return found_requests

    def __trim_grave_accent(self, href):
        """Trim grave accents manually (because BeautifulSoup doesn't support it).

        Args:
            href (str): The BeautifulSoup href value.

        Returns:
            str: The BeautifulSoup href value without grave accents.

        """

        if href.startswith("`"):
            href = href[1:]

        if href.endswith("`"):
            href = href[:-1]

        return href
