import datetime 
import logging
import os
import requests

from dotenv import load_dotenv

from src.data_service.reader import _BaseReader


load_dotenv()
logger = logging.getLogger(__name__)


class TiingoReader(_BaseReader):
    """Stock market OHLC data from https://www.tiingo.com/"""
    def __init__(self, ctx) -> None:
        super().__init__()
        self.ctx = ctx
        self.key = os.getenv('TIINGO_KEY')
        self.url = ctx.obj['data_service']['url_tiingo']

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'ctx={self.ctx}, '
            f'key={self.key}, '
            f'start={self.start}, '
            f'symbol={self.symbol}, '
            f'url={self.url})'
            )

    def download(self):
        """"""
        if self.ctx.obj['default']['debug'] == 'True':
            logger.debug(f"download({self})")
        for symbol in self.symbol:
            yield self._parse_price_data(symbol)

    def _parse_price_data(self, symbol):
        if self.ctx.obj['default']['debug'] == 'True':
            logger.debug(f"_parse_price_data(symbol={symbol})")

        data_list = []
        for item in self._read_one_price_data(symbol):
            data = [
                datetime.date.fromisoformat(item.get('date')[:10]),
                symbol.upper(),
                round(item.get('adjOpen')*100),
                round(item.get('adjHigh')*100),
                round(item.get('adjLow')*100),
                round(item.get('adjClose')*100),
                item.get('adjVolume')
            ]
            data_list.append(data)

        if self.ctx.obj['default']['debug'] == 'True':
            logger.debug(f"_parse_price_data() --> data_list:\n{data_list}")
        return data_list
    
    def _read_one_price_data(self, symbol):
        """"""
        headers = {
            'Content-Type': 'application/json'
        }
        requestResponse = requests.get(
            f"{self.url}/daily/"
            f"{symbol}/prices?"
            f"startDate={self.start}"
            f"&token={self.key}", 
            headers=headers
            )
        if self.ctx.obj['default']['debug'] == 'True':
            logger.debug(f"_read_one_price_data(symbol={symbol}) --> requestResponse:\n{requestResponse.json()}")
        return requestResponse.json()
    

# import json
# import os
# import requests
# from datetime import date

# from dotenv import load_dotenv

# from src.data_service import _BaseReader


# load_dotenv()


# class AlphaReader(_BaseReader):
#     """"""
#     def __init__(self) -> None:
#         super().__init__()
#         self.api_key = os.getenv('ALPHA_KEY')


# class TiingoReader(_BaseReader):
#     """"""
#     def __init__(self) -> None:
#         super().__init__()
#         self.api_key = os.getenv('TIINGO_KEY')
#         self.freq = 'daily'

#     @property
#     def params(self):
#         """Parameters to use in API calls"""
#         return {
#             'startDate'
#             # "startDate": self.start.strftime("%Y-%m-%d"),
#             # "endDate": self.end.strftime("%Y-%m-%d"),
#             # "resampleFreq": self.freq,
#             # "format": "json",
#         }

#     @property
#     def base_url(self):
#         """API URL"""
#         return "https://api.tiingo.com/tiingo"

#     def _read_one_price_data(self, symbol):
#         """"""
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Token {self.api_key}',
#         }
#         data = requests.get(f"{self.base_url}/{self.freq}/{symbol}/prices?startDate={self.start}&endDate={self.end}&token={self.api_key}", headers=headers)
#         return data.json()

#     # def parse_price_data(self, symbol):
#     #     """Returns a list of lists"""
#     #     data_list = []
#     #     for item in self._read_one_price_data(symbol):
#     #         data = [
#     #             date(*map(int, item.get('date')[:10].split('-'))),
#     #             symbol.upper(),
#     #             round(item.get('adjOpen')*100),
#     #             round(item.get('adjHigh')*100),
#     #             round(item.get('adjLow')*100),
#     #             round(item.get('adjClose')*100),
#     #             item.get('adjVolume'),
#     #         ]
#     #         data_list.append(data)
#     #     return data_list

#     def parse_price_data(self, symbol):
#         """Returns a generator object"""
#         for item in self._read_one_price_data(symbol):
#             data = [
#                 date(*map(int, item.get('date')[:10].split('-'))),
#                 symbol.upper(),
#                 round(item.get('adjOpen')*100),
#                 round(item.get('adjHigh')*100),
#                 round(item.get('adjLow')*100),
#                 round(item.get('adjClose')*100),
#                 item.get('adjVolume'),
#             ]
#             yield data
