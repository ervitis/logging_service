# -*- coding: utf-8 -*-

import unittest

import logging_service


def delete_file(file_name):
    import os

    os.remove(file_name)


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.srv_file = logging_service.FileLogging(level=logging_service.ERROR)

    def tearDown(self):
        delete_file('log.log')

    def test_functional_file_handler(self):
        message = 'Hello world'
        logging_service.Logging.set_services([self.srv_file]).send(message)

        with open('log.log', 'r') as my_log_file:
            lines = my_log_file.readlines()

            for line in lines:
                self.assertIn(message, line)


if __name__ == '__main__':
    unittest.main()
