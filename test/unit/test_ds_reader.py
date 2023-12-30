import logging
import unittest
from unittest.mock import MagicMock

from test.data import (
    ctx, read_one_price_data_IWM, read_one_price_data_LQD, 
    parse_price_data_IWM, parse_price_data_LQD, symbol
)
from src import config_dict
from src.data_service.reader import TiingoReader

debug = config_dict['default']['debug'] == 'True'
logger = logging.getLogger(__name__)


class TiingoReaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ctx = MagicMock()
        self.ctx.return_value = ctx
        self.read_one_price_data_IWM = MagicMock()
        self.read_one_price_data_IWM.return_value = read_one_price_data_IWM
        self.parse_price_data_IWM = MagicMock()
        self.parse_price_data_IWM.return_value = parse_price_data_IWM
        self.read_one_price_data_LQD = MagicMock()
        self.read_one_price_data_LQD.return_value = read_one_price_data_LQD
        self.parse_price_data_LQD = MagicMock()
        self.parse_price_data_LQD.return_value = parse_price_data_LQD
        self.get_data = MagicMock()
        # self.get_data.return_value = get_data
        self.symbol = MagicMock()
        self.symbol.return_value = symbol

    def tearDown(self) -> None:
        # logging.disable(logging.CRITICAL)
        del self

    @unittest.skip
    def test_fetch_data_list(self):
        tiingo_data = TiingoReader.fetch_data_list(self)
        for i in range(len(self.get_data.return_value)):
            if debug: logger.debug(f"next(tiingo_data): {tiingo_data}")
        #     print(f"\n\ntiingo_data, self.get_data.return_value[{i}]={tiingo_data, self.get_data.return_value[i][1]}\n")
        #     # self.assertEqual(tiingo_data, self.get_data.return_value[i][1])
        # for i, j in enumerate(self.get_data.return_value):
        # # for i, j in enumerate(tiingo_data):
        #     print(f"\ndata[{i}]={j}")

if __name__ == '__main__':
    unittest.main(verbosity=2)