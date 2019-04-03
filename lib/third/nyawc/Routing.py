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

import re

class Routing(object):
    """The Routing class counts requests that match certain routes.

    Attributes:
        __routing_options (:class:`nyawc.OptionsRouting`): The options containing routing information.
        __routing_count (obj): The {key: value} dict that contains the amount of requests for certain routes.

    """

    def __init__(self, options):
        """Constructs a Crawler instance.

        Args:
            options (:class:`nyawc.Options`): The options to use for the current crawling runtime.

        """

        self.__routing_options = options.routing
        self.__routing_count = {}

    def increase_route_count(self, crawled_request):
        """Increase the count that determines how many times a URL of a certain route has been crawled.

        Args:
            crawled_request (:class:`nyawc.http.Request`): The request that possibly matches a route.

        """

        for route in self.__routing_options.routes:
            if re.compile(route).match(crawled_request.url):
                count_key = str(route) + crawled_request.method
                
                if count_key in self.__routing_count.keys():
                    self.__routing_count[count_key] += 1
                else:
                    self.__routing_count[count_key] = 1

                break

    def is_treshold_reached(self, scraped_request):
        """Check if similar requests to the given requests have already been crawled X times. Where X is the 
        minimum treshold amount from the options.

        Args:
            scraped_request (:class:`nyawc.http.Request`): The request that possibly reached the minimum treshold.

        Returns:
            bool: True if treshold reached, false otherwise.

        """

        for route in self.__routing_options.routes:
            if re.compile(route).match(scraped_request.url):
                count_key = str(route) + scraped_request.method

                if count_key in self.__routing_count.keys():
                    return self.__routing_count[count_key] >= self.__routing_options.minimum_threshold
                
        return False
