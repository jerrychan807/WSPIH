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

class CrawlerActions(object):
    """The actions that crawler callbacks can return.

    Attributes:
        DO_CONTINUE_CRAWLING (int): Continue by crawling the request.
        DO_SKIP_TO_NEXT (int): Skip the current request and continue with the next one in line.
        DO_STOP_CRAWLING (int): Stop crawling and quit ongoing requests.
        DO_AUTOFILL_FORM (int): Autofill this form with random values.
        DO_NOT_AUTOFILL_FORM (int): Do not autofill this form with random values.

    """

    DO_CONTINUE_CRAWLING = 1

    DO_SKIP_TO_NEXT = 2

    DO_STOP_CRAWLING = 3

    DO_AUTOFILL_FORM = 4

    DO_NOT_AUTOFILL_FORM = 5
