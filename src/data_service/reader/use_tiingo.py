import os

from dotenv import load_dotenv

from src.data_service.reader import _BaseReader

load_dotenv()


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
            f'url={self.url})'
            )

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
