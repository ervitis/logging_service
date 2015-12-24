# -*- coding: utf-8 -*-


from __future__ import print_function
import functools
import logging
from logging.handlers import HTTPHandler


def track_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.is_called = True
        return func(*args, **kwargs)
    wrapper.is_called = False
    return wrapper


class FunctionNotCalledError(Exception):

    def __init__(self, message):
        super(FunctionNotCalledError, self).__init__(message)


class Logging(object):
    _srvs = []

    @classmethod
    def init(cls, srvs):
        cls._srvs = srvs
        return cls

    @classmethod
    def send(cls, message):
        for srv in cls._srvs:
            srv.send_message(message)
        return cls


class LoggingInterface(object):

    def __init__(self):
        pass

    def send_message(self, message):
        raise NotImplementedError

    def _set_handler(self, formatter):
        raise NotImplementedError

    def _set_formatter(self):
        raise NotImplementedError


class StreamLogging(LoggingInterface):

    def __init__(self):
        super(StreamLogging, self).__init__()
        self._logger = logging.getLogger('StreamLogging')
        formater = self._set_formatter()
        handler = self._set_handler(formater)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def send_message(self, message):
        self._logger.debug(message)

    def _set_handler(self, formatter):
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class PostLogging(LoggingInterface):

    def __init__(self):
        super(PostLogging, self).__init__()
        self._logger = logging.getLogger('PostLogging')
        formater = self._set_formatter()
        handler = self._set_handler(formater)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def send_message(self, message):
        self._logger.debug(message)

    def _set_handler(self, formatter):
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FileLogging(LoggingInterface):

    def __init__(self):
        super(FileLogging, self).__init__()
        self._logger = logging.getLogger('FileLogging')
        formatter = self._set_formatter()
        handler = self._set_handler(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def send_message(self, message):
        self._logger.debug(message)

    def _set_handler(self, formatter):
        import os
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'my_log.log'
        )
        handler = logging.FileHandler(path)
        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    srvStream = StreamLogging()
    srvFile = FileLogging()

    my_services = [srvStream, srvFile]
    Logging.init(srvs=my_services).send('This is a PoC to try my logging service')
    Logging.send('This is another sentence I send')

    my_services = [srvFile]
    Logging.init(srvs=my_services)
    Logging.send('This is my last message')
