import datetime
import logging
import unittest
# from unittest.mock import Mock


class DataServiceClientTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data = []

    def tearDown(self) -> None:
        logging.disable(logging.CRITICAL)
        del self.data

    def test_client(self):
        pass


if __name__ == '__main__':
    unittest.main()
