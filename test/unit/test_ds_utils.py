import datetime
import logging
import unittest
from unittest.mock import Mock

# from src.data_service.utils import 


class DataServiceUtilsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data = [
            [
                [datetime.date(2023, 11, 21), 'EEM', 3975, 3983, 3952, 3960, 20929670], 
                [datetime.date(2023, 11, 22), 'EEM', 3955, 3964, 3938, 3952, 20007157], 
                [datetime.date(2023, 11, 24), 'EEM', 3936, 3957, 3933, 3954, 11365033]], 
            [
                [datetime.date(2023, 11, 21), 'IWM', 17824, 17850, 17691, 17702, 30457019], 
                [datetime.date(2023, 11, 22), 'IWM', 17818, 17939, 17742, 17813, 28980363], 
                [datetime.date(2023, 11, 24), 'IWM', 17805, 17973, 17780, 17933, 13846889]], 
            [
                [datetime.date(2023, 11, 21), 'LQD', 10483, 10497, 10455, 10484, 20273258], 
                [datetime.date(2023, 11, 22), 'LQD', 10524, 10538, 10485, 10526, 18587992], 
                [datetime.date(2023, 11, 24), 'LQD', 10486, 10502, 10470, 10472, 6391351]]
            ]

    def tearDown(self) -> None:
        logging.disable(logging.CRITICAL)
        del self.data

    def test_parse_price_data(self):
        print(f"\ndata: {self.data}")


if __name__ == '__main__':
    unittest.main()