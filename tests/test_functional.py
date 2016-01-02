# -*- coding: utf-8 -*-

import unittest

import logging_service
from logging_service import Logging


def delete_file(file_name):
    import os

    os.remove(file_name)


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        delete_file('log.log')

    def test_functional_file_handler(self):
        srv_file = logging_service.FileLogging()
        message = 'Hello world'
        Logging.set_services([srv_file]).send(message)

        Logging.send('Another message', level=logging_service.ERROR)

        with open('log.log', 'r') as my_log_file:
            lines = my_log_file.readlines()

            for line in lines:
                self.assertIn('DEBUG', line)


if __name__ == '__main__':
    unittest.main()
