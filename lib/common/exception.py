#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2019/4/15 12:14 AM
# @Author  : Jerry
# @Desc    : 
# @File    : exception.py

def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

                # re-raise the exception
                # raise err

        return wrapper

    return decorator
