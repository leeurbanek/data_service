import logging

from src import debug
from src.data_service.utils import DatabaseConnectionManager


logger = logging.getLogger(__name__)


def get_data(ctx):
    """"""
    if debug: logger.debug(f"get_data(ctx={ctx})")

    # select data provider
    if ctx.obj['data_service']['provider'] == 'alpha':
        data_generator = _use_alpha_reader(ctx)
    elif ctx.obj['data_service']['provider'] == 'tiingo':
        data_generator = _use_tiingo_reader(ctx)

    if debug: logger.debug(f"-> {data_generator}")

    for i, item in enumerate(data_generator):
        print(f"processing item {i+1}, {item}")


def _use_alpha_reader(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True': logger.debug(f"_use_alpha_reader(ctx={ctx.obj}) -> generator object")
    
    from src.data_service.reader.alphavantage import AlphavantageReader
    reader = AlphavantageReader(ctx)
    data_generator = (  # generator object of ohlc price data
        reader.get_data_tuple(symbol) 
        for symbol in ctx.obj['data_service']['symbol']
    )
    return data_generator


def _use_tiingo_reader(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True': logger.debug(f"_use_tiingo_reader(ctx={ctx.obj}) -> generator object")

    from src.data_service.reader.tiingo import TiingoReader
    reader = TiingoReader(ctx)
    data_generator = (  # generator object of ohlc price data
        reader.get_data_tuple(symbol) 
        for symbol in ctx.obj['data_service']['symbol']
    )
    return data_generator
