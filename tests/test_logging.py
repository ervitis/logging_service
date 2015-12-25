# -*- coding: utf-8 -*-


import unittest

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


if __name__ == '__main__':
    unittest.main()
