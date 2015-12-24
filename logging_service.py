# -*- coding: utf-8 -*-


from __future__ import print_function
import functools
import logging

from logging.handlers import HTTPHandler

METHODS = ['POST', 'GET']


__all__ = [
    'FileLogging', 'Logging', 'PostLogging', 'StreamLogging'
]
__version__ = '1.1.1'


def track_function_call(func):
    # When you want to track the developer if some function has been called
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.is_called = True
        return func(*args, **kwargs)
    wrapper.is_called = False
    return wrapper


class FunctionNotCalledError(Exception):

    def __init__(self, message):
        super(FunctionNotCalledError, self).__init__(message)


class MethodNotAllowedError(Exception):

    def __init__(self, message):
        super(MethodNotAllowedError, self).__init__(message)


class Logging(object):
    _srvs = []

    @classmethod
    def set_services(cls, srvs):
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

    def __init__(self, host, port, url_path, method='POST'):
        super(PostLogging, self).__init__()
        self._host = host

        if isinstance(port, int):
            port = str(port)

        self._port = port
        self._url_path = url_path
        self._method = method

        self._logger = logging.getLogger('PostLogging')
        formater = self._set_formatter()
        handler = self._set_handler(formater)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def send_message(self, message):
        import json

        data = {
            'type': 'debug',
            'msg': message
        }
        self._logger.debug(json.dumps(data))

    def _set_handler(self, formatter):
        host = self._host + ':' + self._port

        if not self._check_method_is_valid():
            raise MethodNotAllowedError('The method %s is not allowed. Use %s' % (self._method, ','.join(METHODS)))

        handler = HTTPHandler(host, self._url_path, method='POST')
        handler.setFormatter(formatter)
        return handler

    def _check_method_is_valid(self):
        method = self._method.upper()
        return False if method not in METHODS else True

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FileLogging(LoggingInterface):

    def __init__(self, path_file_name=None):
        super(FileLogging, self).__init__()
        self._path_file = path_file_name if path_file_name else 'log.log'
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
            self._path_file
        )
        handler = logging.FileHandler(path)
        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    srvStream = StreamLogging()
    srvFile = FileLogging()
    srvPost = PostLogging(url_path='/message', host='127.0.0.1', port=8000)

    my_services = [srvStream, srvFile, srvPost]
    Logging.set_services(srvs=my_services).send('This is a PoC to try my logging service')
    Logging.send('This is another sentence I send')

    my_services = [srvFile]
    Logging.set_services(srvs=my_services)
    Logging.send('This is my last message')

    my_services = [srvPost]
    Logging.set_services(my_services)
    Logging.send('I send a message')

    my_services = [srvPost, srvFile, srvStream]
    Logging.set_services(my_services)
    Logging.send('Some characters: ñÑ%&/()=?¿\ª')
