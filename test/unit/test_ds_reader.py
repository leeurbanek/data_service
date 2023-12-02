import datetime
import logging
import unittest
from unittest.mock import Mock

from src.data_service.reader.tiingo import TiingoReader


class TiingoReaderTest(unittest.TestCase):

    def setUp(self) -> None:
        # self.ctx.obj['default']['debug'] = Mock()
        # self.ctx.obj['default']['debug'].return_value = 'True'
        # self.ctx = Mock()
        # self.ctx.return_value = {
        self.ctx = {
            'default': {
                'debug': 'True', 
                'temp_dir': 'temp'
            }, 
            'data_service': {
                'back_days': '5', 
                'database': 'db.sqlite', 
                'symbol': 'EEM IWM LQD', 
                'url_tiingo': 'https://api.tiingo.com/tiingo'
            }
        }
        self._read_one_price_data = Mock()
        self._read_one_price_data.return_value = [
            {
                'date': '2023-11-21T00:00:00.000Z', 
                'close': 39.6, 
                'high': 39.83, 
                'low': 39.52, 
                'open': 39.75, 
                'volume': 20929670, 
                'adjClose': 39.6, 
                'adjHigh': 39.83, 
                'adjLow': 39.52, 
                'adjOpen': 39.75, 
                'adjVolume': 20929670, 
                'divCash': 0.0, 
                'splitFactor': 1.0
            }, 
            {
                'date': '2023-11-22T00:00:00.000Z', 
                'close': 39.52, 
                'high': 39.64, 
                'low': 39.38, 
                'open': 39.55, 
                'volume': 20007157, 
                'adjClose': 39.52, 
                'adjHigh': 39.64, 
                'adjLow': 39.38, 
                'adjOpen': 39.55, 
                'adjVolume': 20007157, 
                'divCash': 0.0, 
                'splitFactor': 1.0
            }, 
            {
                'date': '2023-11-24T00:00:00.000Z', 
                'close': 39.54, 
                'high': 39.57, 
                'low': 39.33, 
                'open': 39.36, 
                'volume': 11365033, 
                'adjClose': 39.54, 
                'adjHigh': 39.57, 
                'adjLow': 39.33, 
                'adjOpen': 39.36, 
                'adjVolume': 11365033, 
                'divCash': 0.0, 
                'splitFactor': 1.0
            }
        ]

    def tearDown(self) -> None:
        logging.disable(logging.CRITICAL)
        del self._read_one_price_data

    def test_parse_price_data(self):
        data_list = [datetime.date(2023, 3, 31), 'IWM', 17640, 17864, 17637, 17840, 39602850]
        self.assertEqual(TiingoReader._read_one_price_data(self.ctx, 'IWM'), data_list)


if __name__ == '__main__':
    unittest.main()