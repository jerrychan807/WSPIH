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

from collections import OrderedDict

import tldextract

try: # Python 3
    from urllib.parse import urljoin, urlparse, parse_qsl, urlencode, urlunparse
except: # Python 2
    from urllib import urlencode
    from urlparse import urljoin, urlparse, parse_qsl, urlunparse

class URLHelper:
    """A helper for URL strings.

    Attributes:
        __cache (obj): Cached values of parsed URL data.

    """

    __cache = {}

    @staticmethod
    def make_absolute(base, relative):
        """Make the given (relative) URL absolute.

        Args:
            base (str): The absolute URL the relative url was found on.
            relative (str): The (possibly relative) url to make absolute.

        Returns:
            str: The absolute URL.

        """

        # Python 3.4 and lower do not remove folder traversal strings.
        # This was fixed in 3.5 (https://docs.python.org/3/whatsnew/3.5.html#urllib)
        while relative.startswith('/../') or relative.startswith('../'):
            relative = relative[3:]

            base_parsed = urlparse(base)
            new_path = base_parsed.path.rsplit('/', 1)[0]
            base_parsed = base_parsed._replace(path=new_path)
            base = base_parsed.geturl()

        return urljoin(base, relative)

    @staticmethod
    def append_with_data(url, data):
        """Append the given URL with the given data OrderedDict.

        Args:
            url (str): The URL to append.
            data (obj): The key value OrderedDict to append to the URL.

        Returns:
            str: The new URL.

        """

        if data is None:
            return url

        url_parts = list(urlparse(url))

        query = OrderedDict(parse_qsl(url_parts[4], keep_blank_values=True))
        query.update(data)

        url_parts[4] = URLHelper.query_dict_to_string(query)

        return urlunparse(url_parts)

    @staticmethod
    def is_mailto(url):
        """Check if the given URL is a mailto URL

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if mailto, False otherwise.

        """

        return url.startswith("mailto:")

    @staticmethod
    def is_parsable(url):
        """Check if the given URL is parsable (make sure it's a valid URL). If it is parsable, also cache it.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if parsable, False otherwise.

        """

        try:
            parsed = urlparse(url)
            URLHelper.__cache[url] = parsed
            return True
        except:
            return False

    @staticmethod
    def get_protocol(url):
        """Get the protocol (e.g. http, https or ftp) of the given URL.

        Args:
            url (str): The URL to get the protocol from.

        Returns:
            str: The URL protocol

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        return URLHelper.__cache[url].scheme

    @staticmethod
    def get_subdomain(url):
        """Get the subdomain of the given URL.

        Args:
            url (str): The URL to get the subdomain from.

        Returns:
            str: The subdomain(s)

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        # return (tldextract.extract(url).subdomain)
        return ".".join(URLHelper.__cache[url].netloc.split(".")[:-2])

    @staticmethod
    def get_hostname(url):
        """Get the hostname of the given URL.

        Args:
            url (str): The URL to get the hostname from.

        Returns:
            str: The hostname

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        parts = URLHelper.__cache[url].netloc.split(".")

        if len(parts) == 1:
            return parts[0]
        else:
            return ".".join(parts[-2:-1])
        # return (tldextract.extract(url).domain)

    @staticmethod
    def get_tld(url):
        """Get the tld of the given URL.

        Args:
            url (str): The URL to get the tld from.

        Returns:
            str: The tld

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        parts = URLHelper.__cache[url].netloc.split(".")

        if len(parts) == 1:
            return ""
        else:
            return parts[-1]

    @staticmethod
    def get_path(url):
        """Get the path (e.g /page/23) of the given URL.

        Args:
            url (str): The URL to get the path from.

        Returns:
            str: The path

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        return URLHelper.__cache[url].path

    @staticmethod
    def get_ordered_params(url):
        """Get the query parameters of the given URL in alphabetical order.

        Args:
            url (str): The URL to get the query parameters from.

        Returns:
            str: The query parameters

        """

        if url not in URLHelper.__cache:
            URLHelper.__cache[url] = urlparse(url)

        params = URLHelper.query_string_to_dict(URLHelper.__cache[url].query)

        return OrderedDict(sorted(params.items()))

    @staticmethod
    def remove_hash(url):
        """Remove the #hash from the given URL.

        Args:
            url (str): The URL to remove the hash from.

        Returns:
            str: The URL without the hash

        """

        return url.split("#")[0]

    @staticmethod
    def query_dict_to_string(query):
        """Convert an OrderedDict to a query string.

        Args:
            query (obj): The key value object with query params.

        Returns:
            str: The query string.

        Note:
            This method does the same as urllib.parse.urlencode except
            that it doesn't actually encode the values.

        """

        query_params = []

        for key, value in query.items():
            query_params.append(key + "=" + value)

        return "&".join(query_params)

    @staticmethod
    def query_string_to_dict(query):
        """Convert a string to a query dict.

        Args:
            query (str): The query string.

        Returns:
            obj: The key value object with query params.

        Note:
            This method does the same as urllib.parse.parse_qsl except
            that it doesn't actually decode the values.

        """

        query_params = {}

        for key_value in query.split("&"):
            key_value_pair = key_value.split("=", 1)

            key = key_value_pair[0] if len(key_value_pair) >= 1 else ""
            value = key_value_pair[1] if len(key_value_pair) == 2 else ""

            query_params[key] = value

        return query_params
