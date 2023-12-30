import logging
from collections import namedtuple

from src import debug
# from src.data_service.utils_sqlite import DatabaseConnectionManager
# from test.data import parse_price_data_IWM as tuple_list


logger = logging.getLogger(__name__)


def close_weighted_price(tuple_list):
    """"""
    if debug: logger.debug(f"close_weighted_price(tuple_list={tuple_list})")

    Price = namedtuple('Price', ['symbol', 'date', 'price'])
    price_list =[]

    for item in tuple_list:
        close_weighted_price = Price(
            item.symbol,
            item.date,
            round((item.high + item.low + item.close * 2) / 4)
        )
        price_list.append(close_weighted_price)
    
    if debug: logger.debug(f"close_weighted_price() -> price_list:\n{price_list})")

    return price_list


def volume_data(tuple_list):
    """"""
    if debug: logger.debug(f"volume_data(tuple_list={tuple_list})")

    Volume = namedtuple('Volume', ['symbol', 'date', 'volume'])
    volume_list =[]

    for item in tuple_list:
        volume = Volume(
            item.symbol,
            item.date,
            item.volume
        )
        volume_list.append(volume)
    
    if debug: logger.debug(f"volume_data() -> volume_list:\n{volume_list})")

    return volume_list


# if __name__ == '__main__':
#     close_weighted_price(tuple_list)
#     volume_data(tuple_list)
