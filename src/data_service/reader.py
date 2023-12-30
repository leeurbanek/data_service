import datetime 
import logging
import os
import requests
from collections import namedtuple

from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)


class AlphavantageReader():
    """Retrieve stock market OHLC data from .
    ------------------------------------------------------------
    Instance uses public method `get_data_tuple(symbol)` to return a list.\n
    Parameters
    ----------
    `ctx` : dictionary
        python-click command line interface context dictionary\n
    Returns
    -------
    python list of named tuples\n
    """
    def __init__(self, ctx) -> None:
        self.back_days = ctx.obj['data_service']['back_days']
        self.debug = ctx.obj['default']['debug'] == 'True'
        self.freq = ctx.obj['data_service']['frequency']
        self.key = os.getenv('ALPHA_KEY')
        self.start = self._default_start_date
        self.url = self._url

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"back_days={self.back_days}, "
            f"debug={self.debug}, "
            f"freq={self.freq}, "
            f"key={self.key}, "
            f"start={self.start}, "
            f"url={self._url})"
            )

    @property
    def _default_start_date(self):
        """"""
        lookback = int(self.back_days)
        return datetime.date.today() - datetime.timedelta(days=lookback)

    @property
    def _url(self):
        """API url"""
        return ""
    
    def get_data_tuple(self, symbol):
        """AlphavantageReader.get_data_tuple()
        -----------------------------
        Public method of TiingoReader class. Takes a ticker symbol string.\n
        Returns
        -------
        python namedtuple('symbol', 'date', 'open', 'high', 'low', 'close', 'volume')\n
        """
        if self.debug: logger.debug(f"get_data_tuple(self={self}, symbol={symbol})")
        return self._parse_price_data(symbol)

    def _parse_price_data(self, symbol: str) -> list:
        """"""
        OHLC = namedtuple('OHLC', ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])
        ohlc_list = []

        for item in self._read_one_price_data(symbol):
            data = OHLC(
                symbol.upper(),
                # datetime.date.fromisoformat(item.get('date')[:10]),
                datetime.date.fromisoformat(item.get('date')[:10]).toordinal(),
                round(item.get('adjOpen')*100),
                round(item.get('adjHigh')*100),
                round(item.get('adjLow')*100),
                round(item.get('adjClose')*100),
                item.get('adjVolume')
            )
            ohlc_list.append(data)
        if self.debug: logger.debug(f"_parse_price_data(self, symbol={symbol}) -> namedtuple list:\n{ohlc_list}")
        return ohlc_list

    def _read_one_price_data(self, symbol):
        symbol = [
            {'date': '2023-12-11T00:00:00.000Z', 'close': 187.19, 'high': 187.62, 'low': 185.885, 'open': 186.68, 'volume': 29302064, 'adjClose': 187.19, 'adjHigh': 187.62, 'adjLow': 185.885, 'adjOpen': 186.68, 'adjVolume': 29302064, 'divCash': 0.0, 'splitFactor': 1.0}, 
            {'date': '2023-12-12T00:00:00.000Z', 'close': 187.0, 'high': 187.655, 'low': 185.335, 'open': 186.97, 'volume': 32023999, 'adjClose': 187.0, 'adjHigh': 187.655, 'adjLow': 185.335, 'adjOpen': 186.97, 'adjVolume': 32023999, 'divCash': 0.0, 'splitFactor': 1.0}, 
            {'date': '2023-12-13T00:00:00.000Z', 'close': 193.33, 'high': 193.64, 'low': 185.67, 'open': 187.1, 'volume': 69484819, 'adjClose': 193.33, 'adjHigh': 193.64, 'adjLow': 185.67, 'adjOpen': 187.1, 'adjVolume': 69484819, 'divCash': 0.0, 'splitFactor': 1.0}, 
            {'date': '2023-12-14T00:00:00.000Z', 'close': 198.71, 'high': 200.035, 'low': 196.48, 'open': 196.87, 'volume': 83649334, 'adjClose': 198.71, 'adjHigh': 200.035, 'adjLow': 196.48, 'adjOpen': 196.87, 'adjVolume': 83649334, 'divCash': 0.0, 'splitFactor': 1.0}, 
            {'date': '2023-12-15T00:00:00.000Z', 'close': 197.04, 'high': 199.55, 'low': 195.95, 'open': 198.95, 'volume': 74160699, 'adjClose': 197.04, 'adjHigh': 199.55, 'adjLow': 195.95, 'adjOpen': 198.95, 'adjVolume': 74160699, 'divCash': 0.0, 'splitFactor': 1.0}
        ]
        if self.debug: logger.debug(f"_read_one_price_data(self, symbol={symbol}) -> request response:\n")
        return symbol


class TiingoReader():
    """Retrieve stock market OHLC data from https://www.tiingo.com/.
    ------------------------------------------------------------
    Instance uses public method `get_data_tuple(symbol)` to return a list.\n
    Parameters
    ----------
    `ctx` : dictionary
        python-click command line interface context dictionary\n
    Returns
    -------
    python list of named tuples\n
    """
    def __init__(self, ctx) -> None:
        self.back_days = ctx.obj['data_service']['back_days']
        self.debug = ctx.obj['default']['debug'] == 'True'
        self.freq = ctx.obj['data_service']['frequency']
        self.key = os.getenv('TIINGO_KEY')
        self.start = self._default_start_date
        self.url = self._url

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"back_days={self.back_days}, "
            f"debug={self.debug}, "
            f"freq={self.freq}, "
            f"key={self.key}, "
            f"start={self.start}, "
            f"url={self._url})"
            )

    @property
    def _default_start_date(self):
        """"""
        lookback = int(self.back_days)
        return datetime.date.today() - datetime.timedelta(days=lookback)

    @property
    def _url(self):
        """API url"""
        return "https://api.tiingo.com/tiingo"
    
    def get_data_tuple(self, symbol: str) -> tuple:
        """TiingoReader.get_data_tuple()
        -----------------------------
        Public method of TiingoReader class. Takes a ticker symbol string.\n
        Returns
        -------
        python namedtuple('symbol', 'date', 'open', 'high', 'low', 'close', 'volume')\n
        """
        if self.debug: logger.debug(f"get_data_tuple(self={self}, symbol={symbol})")
        return self._parse_price_data(symbol)

    def _parse_price_data(self, symbol: list) -> list:
        """"""
        OHLC = namedtuple('OHLC', ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])
        ohlc_list = []

        for item in self._read_one_price_data(symbol):
            data = OHLC(
                symbol.upper(),
                # datetime.date.fromisoformat(item.get('date')[:10]),
                datetime.date.fromisoformat(item.get('date')[:10]).toordinal(),
                round(item.get('adjOpen')*100),
                round(item.get('adjHigh')*100),
                round(item.get('adjLow')*100),
                round(item.get('adjClose')*100),
                item.get('adjVolume')
            )
            ohlc_list.append(data)
        if self.debug: logger.debug(f"_parse_price_data(self, symbol={symbol}) -> namedtuple list:\n{ohlc_list}")
        return ohlc_list
    
    def _read_one_price_data(self, symbol):
        """"""
        headers = {
            'Content-Type': 'application/json'
        }
        request_response = requests.get(
            f"{self.url}/{self.freq}/"
            f"{symbol}/prices?"
            f"startDate={self.start}"
            f"&token={self.key}", 
            headers=headers
            )
        if self.debug: logger.debug(f"_read_one_price_data(self, symbol={symbol}) -> request response:\n{request_response.json()}")
        return request_response.json()
