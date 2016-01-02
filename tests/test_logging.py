# -*- coding: utf-8 -*-


import unittest
import os

import logging_service
from logging_service import Logging


def delete_file(file_name):
    os.remove(file_name)


class TestLogging(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists('log.log'):
            delete_file('log.log')

    def test_logging_cls(self):
        self.assertIsNotNone(Logging)

    def test_logging_set_services(self):
        test_service = None

        Logging.set_services([test_service])

        self.assertIn(test_service, Logging._srvs)

    def test_send_message_attribute_error_service_is_none(self):
        test_service = None

        Logging.set_services([test_service])

        with self.assertRaises(AttributeError):
            Logging.send('Hello', logging_service.DEBUG)

    def test_level_valid(self):
        level = logging_service.ERROR

        self.assertTrue(logging_service._level_is_valid(level))

    def test_level_not_valid(self):
        level = 100

        self.assertFalse(logging_service._level_is_valid(level))

    def test_raise_level_not_valid(self):
        level = 100

        with self.assertRaises(logging_service.LevelNotValidError):
            logging_service._raise_level_error_if_not_valid(level)

    def test_level_valid_except_not_raised(self):
        level = logging_service.DEBUG

        try:
            logging_service._raise_level_error_if_not_valid(level)
        except logging_service.LevelNotValidError:
            self.fail()

    def test_filelogging_formatter(self):
        srv_filelogging = logging_service.FileLogging()

        formatter = srv_filelogging._set_formatter()

        import logging
        self.assertIsInstance(formatter, logging.Formatter)

    def test_filelogging_handler(self):
        srv_filelogging = logging_service.FileLogging()

        formatter = srv_filelogging._set_formatter()
        handler = srv_filelogging._set_handler(formatter)

        import logging
        self.assertIsInstance(handler, logging.FileHandler)

    def test_level_changed(self):
        srv_filelogging = logging_service.FileLogging()

        Logging.set_services([srv_filelogging])
        Logging.send('Hello', logging_service.ERROR)

        logging_service._change_level(logging_service.DEBUG)

        Logging.send('Hello', logging_service.INFO)

        with open('log.log', 'r') as test_file:
            lines = test_file.readlines()
            for _ in lines:
                if 'INFO' in _:
                    self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
