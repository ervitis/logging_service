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
__version__ = '2.0.0'


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


def _change_level(level):
    _raise_level_error_if_not_valid(level)

    logging.getLogger().setLevel(level)


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
    def send(cls, message, level):
        for srv in cls._srvs:
            srv.send_message(message, level)
        return cls


class LoggingInterface(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def send_message(self, message, level):
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

    def send_message(self, message, level):
        _change_level(level)

        self._logger.log(msg=message, level=level)

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

    def send_message(self, message, level):
        _change_level(level)

        import json

        data = {
            'type': logging.getLevelName(level),
            'msg': message
        }
        self._logger.log(level=level, msg=json.dumps(data))

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

    def send_message(self, message, level):
        _change_level(level)

        self._logger.log(msg=message, level=level)

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


if __name__ == '__main__':
    srvStream = StreamLogging()
    srvFile = FileLogging()
    srvPost = PostLogging(url_path='/message', host='127.0.0.1', port=8000)

    my_services = [srvStream, srvFile, srvPost]
    Logging.set_services(srvs=my_services).send('This is a PoC to try my logging service', level=WARNING)
    Logging.send('This is another sentence I send', level=DEBUG)

    my_services = [srvFile]
    Logging.set_services(srvs=my_services)
    Logging.send('This is my last message', level=ERROR)

    my_services = [srvPost]
    Logging.set_services(my_services)
    Logging.send('I send a message', level=INFO)

    my_services = [srvPost, srvFile, srvStream]
    Logging.set_services(my_services)
    Logging.send('Some characters: ñÑ%&/()=?¿\ª', level=ERROR)
