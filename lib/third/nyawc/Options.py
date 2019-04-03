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

import requests

from lib.third.nyawc.http.Request import Request
from lib.third.nyawc.helpers.PackageHelper import PackageHelper
from lib.third.nyawc.CrawlerActions import CrawlerActions
from requests_toolbelt import user_agent

class Options(object):
    """The Options class contains all the crawling options.

    Attributes:
        scope (:class:`nyawc.Options.OptionsScope`): Can be used to define the crawling scope.
        callbacks (:class:`nyawc.Options.OptionsCallbacks`): Can be used to define crawling callbacks.
        performance (:class:`nyawc.Options.OptionsPerformance`): Can be used to define performance options.
        identity (:class:`nyawc.Options.OptionsIdentity`): Can be used to define the identity/footprint options.
        routing (:class:`nyawc.Options.OptionsRouting`): Can be used to define routes to ignore similar requests.
        misc (:class:`nyawc.Options.OptionsMisc`): Can be used to define the other options.

    """

    def __init__(self):
        """Constructs an Options instance."""

        self.scope = OptionsScope()
        self.callbacks = OptionsCallbacks()
        self.performance = OptionsPerformance()
        self.identity = OptionsIdentity()
        self.routing = OptionsRouting()
        self.misc = OptionsMisc()

class OptionsScope(object):
    """The OptionsScope class contains the scope options.

    Attributes:
        protocol_must_match (bool): only crawl pages with the same protocol as the startpoint (e.g. only https).
        subdomain_must_match (bool): only crawl pages with the same subdomain as the startpoint, if the startpoint is not a subdomain, no subdomains will be crawled.
        hostname_must_match (bool): only crawl pages with the same hostname as the startpoint (e.g. only `finnwea`).
        tld_must_match (bool): only crawl pages with the same tld as the startpoint (e.g. only `.com`)
        max_depth (obj): the maximum search depth. For example, 2 would be the startpoint and all the pages found on it. Default is None (unlimited).
        request_methods list(str): only crawl these request methods. If empty or ``None`` all request methods will be crawled. Default is all.

    """

    def __init__(self):
        """Constructs an OptionsScope instance."""

        self.protocol_must_match = False
        self.subdomain_must_match = True
        self.hostname_must_match = True
        self.tld_must_match = True
        self.max_depth = None
        self.request_methods = []

class OptionsCallbacks(object):
    """The OptionsCallbacks class contains all the callback methods.

    Attributes:
        crawler_before_start (obj): called before the crawler starts crawling. Default is a null route to :attr:`__null_route_crawler_before_start`.
        crawler_after_finish (obj): called after the crawler finished crawling. Default is a null route to :attr:`__null_route_crawler_after_finish`.
        request_before_start (obj): called before the crawler starts a new request. Default is a null route to :attr:`__null_route_request_before_start`.
        request_after_finish (obj): called after the crawler finishes a request. Default is a null route to :attr:`__null_route_request_after_finish`.
        request_in_thread_before_start (obj): called in the crawling thread (when it started). Default is a null route to :attr:`__null_route_request_in_thread_before_start`.
        request_in_thread_after_finish (obj): called in the crawling thread (when it finished). Default is a null route to :attr:`__null_route_request_in_thread_after_finish`.
        request_on_error (obj): called if a request failed. Default is a null route to :attr:`__null_route_request_on_error`.
        form_before_autofill (obj): called before the crawler starts autofilling a form. Default is a null route to :attr:`__null_route_form_before_autofill`.
        form_after_autofill (obj): called after the crawler finishes autofilling a form. Default is a null route to :attr:`__null_route_form_after_autofill`.

    """

    def __init__(self):
        """Constructs an OptionsCallbacks instance."""

        self.crawler_before_start = self.__null_route_crawler_before_start
        self.crawler_after_finish = self.__null_route_crawler_after_finish
        self.request_before_start = self.__null_route_request_before_start
        self.request_after_finish = self.__null_route_request_after_finish
        self.request_in_thread_before_start = self.__null_route_request_in_thread_before_start
        self.request_in_thread_after_finish = self.__null_route_request_in_thread_after_finish
        self.request_on_error = self.__null_route_request_on_error
        self.form_before_autofill = self.__null_route_form_before_autofill
        self.form_after_autofill = self.__null_route_form_after_autofill

    def __null_route_crawler_before_start(self):
        """A null route for the 'crawler before start' callback."""

        pass

    def __null_route_crawler_after_finish(self, queue):
        """A null route for the 'crawler after finish' callback.

        Args:
            queue (obj): The current crawling queue.

        """

        pass

    def __null_route_request_before_start(self, queue, queue_item):
        """A null route for the 'request before start' callback.

        Args:
            queue (:class:`nyawc.Queue`): The current crawling queue.
            queue_item (:class:`nyawc.QueueItem`): The queue item that's about to start.

        Returns:
            str: A crawler action (either DO_SKIP_TO_NEXT, DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def __null_route_request_after_finish(self, queue, queue_item, new_queue_items):
        """A null route for the 'request after finish' callback.

        Args:
            queue (:class:`nyawc.Queue`): The current crawling queue.
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            new_queue_items list(:class:`nyawc.QueueItem`): The new queue items that were found in the one that finished.

        Returns:
            str: A crawler action (either DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def __null_route_request_in_thread_before_start(self, queue_item):
        """A null route for the 'request in thread before start' callback.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.

        Note:
            This method gets called in the crawling thread and is therefore not thread safe.

        """

        pass

    def __null_route_request_in_thread_after_finish(self, queue_item):
        """A null route for the 'request in thread after finish' callback.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.

        Note:
            This method gets called in the crawling thread and is therefore not thread safe.

        """

        pass

    def __null_route_request_on_error(self, queue_item, message):
        """A null route for the 'request on error' callback.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            message str: The error message.

        """

        pass

    def __null_route_form_before_autofill(self, queue_item, elements, form_data):
        """A null route for the 'form before autofill' callback.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            elements list(obj): The soup elements found in the form.
            form_data (obj): The {key: value} form fields to be autofilled.

        Returns:
            str: A crawler action (either DO_AUTOFILL_FORM or DO_NOT_AUTOFILL_FORM).

        """

        return CrawlerActions.DO_AUTOFILL_FORM

    def __null_route_form_after_autofill(self, queue_item, elements, form_data):
        """A null route for the 'form after autofill' callback.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            elements list(obj): The soup elements found in the form.
            form_data (obj): The {key: value} form fields.

        """

        pass

class OptionsPerformance(object):
    """The OptionsPerformance class contains the performance options.

    Attributes:
        max_threads (obj): the maximum amount of simultaneous threads to use for crawling.
        request_timeout (int): the request timeout in seconds (throws an exception if exceeded).

    """

    def __init__(self):
        """Constructs an OptionsPerformance instance."""

        self.max_threads = 40
        self.request_timeout = 30

class OptionsIdentity(object):
    """The OptionsIdentity class contains the identity/footprint options.

    Attributes:
        auth (obj): The (requests module) authentication class to use when making a request. For more information check http://docs.python-requests.org/en/master/user/authentication/.
        cookies (obj): The (requests module) cookie jar to use when making a request. For more information check http://docs.python-requests.org/en/master/user/quickstart/#cookies.
        headers (obj): The headers {key: value} to use when making a request.
        proxies (obj): The proxies {key: value} to use when making a request. For more information check http://docs.python-requests.org/en/master/user/advanced/#proxies.

    """

    def __init__(self):
        """Constructs an OptionsIdentity instance."""

        self.auth = None
        self.cookies = requests.cookies.RequestsCookieJar()
        self.headers = requests.utils.default_headers()
        self.headers.update({"User-Agent": user_agent(PackageHelper.get_alias(), PackageHelper.get_version())})
        self.proxies = None

class OptionsRouting(object):
    """The OptionsRouting class can contain routes that prevent the crawler from crawling similar pages multiple times.

    Attributes:
        minimum_threshold (int): The minimum amount of requests to crawl (matching a certain route) before ignoring the rest. Default is 20.
        routes (arr): The regular expressions that represent routes that should not be cralwed more times than the minimum treshold. Default is an empty array.

    Note:
        An example would be if you have a news site with URLs like (/news/3443, news/2132, news/9475, etc). You can add a regular expression
        that matches this route so only X requests that match regular expression will be crawled (where X is the minimum treshold).

    Note:
        The crawler will only stop crawling requests of certain routes at exactly the minimum treshold if the maximum threads option is set to 1.
        If the maximum threads option is set to a value higher than 1 the threshold will get a bit higher depending on the amount of threads used.

    """

    def __init__(self):
        """Constructs an OptionsRouting instance."""

        self.minimum_threshold = 20
        self.routes = []


class OptionsMisc(object):
    """The OptionsMisc class contains all kind of misc options.

    Attributes:
        debug (bool): If debug is enabled extra information will be logged to the console. Default is False.
        verify_ssl_certificates (bool): If verification is enabled all SSL certificates will be checked for validity. Default is True.
        trusted_certificates (str): You can pass the path to a CA_BUNDLE file or directory with certificates of trusted CAs. Default is None.

    """

    def __init__(self):
        """Constructs an OptionsMisc instance."""

        self.debug = False
        self.verify_ssl_certificates = True
        self.trusted_certificates = None
