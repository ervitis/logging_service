# -*- coding: utf-8 -*-


import unittest

import logging_service
from logging_service import Logging


class TestLogging(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
            Logging.send('Hello')

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


if __name__ == '__main__':
    unittest.main()
