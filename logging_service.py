# -*- coding: utf-8 -*-


from __future__ import print_function
import functools
import logging
import os

from logging.handlers import HTTPHandler

METHODS = ['POST', 'GET']

INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.ERROR
LOGGING_LEVELS = [INFO, DEBUG, WARNING, ERROR]


__all__ = [
    'DEBUG', 'ERROR', 'FileLogging', 'INFO', 'Logging', 'PostLogging', 'StreamLogging', 'WARNING'
]
__version__ = '1.2.4'


def track_function_call(func):
    # When you want to track the developer if some function has been called
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.is_called = True
        return func(*args, **kwargs)
    wrapper.is_called = False
    return wrapper


def _level_is_valid(level):
    return True if level in LOGGING_LEVELS else False


def _raise_level_error_if_not_valid(level):
    if not _level_is_valid(level):
        raise LevelNotValidError('Level %s is not valid, use %s' % (level, ','.join(str(LOGGING_LEVELS))))


class FunctionNotCalledError(Exception):

    def __init__(self, message):
        super(FunctionNotCalledError, self).__init__(message)


class MethodNotAllowedError(Exception):

    def __init__(self, message):
        super(MethodNotAllowedError, self).__init__(message)


class LevelNotValidError(Exception):

    def __init__(self, message):
        super(LevelNotValidError, self).__init__(message)


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
        self._logger = logging.getLogger(__name__)
        self._level = None

    def send_message(self, message):
        raise NotImplementedError

    def _set_handler(self, formatter):
        raise NotImplementedError

    def _set_formatter(self):
        raise NotImplementedError

    def set_level(self, level):
        self._level = level


class StreamLogging(LoggingInterface):

    def __init__(self, level):
        super(StreamLogging, self).__init__()
        self._logger = logging.getLogger('StreamLogging')
        formater = self._set_formatter()
        handler = self._set_handler(formater)
        self._logger.addHandler(handler)

        self._level = level
        _raise_level_error_if_not_valid(self._level)

        self._logger.setLevel(self._level)

    def send_message(self, message):
        self._logger.log(msg=message, level=self._level)

    def _set_handler(self, formatter):
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_level(self, level):
        super(StreamLogging, self).set_level(level)


class PostLogging(LoggingInterface):

    def __init__(self, level, host, port, url_path, method='POST'):
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

        self._level = level
        _raise_level_error_if_not_valid(self._level)

        self._logger.setLevel(self._level)

    def send_message(self, message):
        import json

        data = {
            'type': logging.getLevelName(self._level),
            'msg': message
        }
        self._logger.log(level=self._level, msg=json.dumps(data))

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

    def set_level(self, level):
        super(PostLogging, self).set_level(level)


class FileLogging(LoggingInterface):

    def __init__(self, level, path_file_name=None):
        super(FileLogging, self).__init__()
        self._path_file = path_file_name if path_file_name else 'log.log'
        self._logger = logging.getLogger('FileLogging')
        formatter = self._set_formatter()
        handler = self._set_handler(formatter)
        self._logger.addHandler(handler)

        self._level = level
        _raise_level_error_if_not_valid(self._level)

        self._logger.setLevel(self._level)

    def send_message(self, message):
        self._logger.log(msg=message, level=self._level)

    def _set_handler(self, formatter):
        if self._path_file:
            handler = logging.FileHandler(self._path_file)
        else:
            path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                self._path_file
            )
            handler = logging.FileHandler(path)

        handler.setFormatter(formatter)
        return handler

    def _set_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_level(self, level):
        super(FileLogging, self).set_level(level)


if __name__ == '__main__':
    srvStream = StreamLogging(level=ERROR)
    srvFile = FileLogging(level=DEBUG)
    srvPost = PostLogging(url_path='/message', host='127.0.0.1', port=8000, level=WARNING)

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
