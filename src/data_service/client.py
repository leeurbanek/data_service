import logging


logger = logging.getLogger(__name__)


def get_data(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"get_data(ctx={ctx})")

    # select data provider
    if ctx.obj['data_service']['provider'] == 'alpha':
        data = use_alpha_reader(ctx)
    elif ctx.obj['data_service']['provider'] == 'tiingo':
        data = use_tiingo_reader(ctx)

        if ctx.obj['default']['debug'] == 'True':
            logger.debug(f"get_data(ctx) --> data:\n {[item for item in data]})")


def use_alpha_reader(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"use_alpha_reader(ctx={ctx.obj})")


def use_tiingo_reader(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"use_tiingo_reader(ctx={ctx})")

    from src.data_service.reader.tiingo import TiingoReader
    reader = TiingoReader(ctx)
    return reader.download()

    # for symbol in ctx.obj['data_service']['symbol']:
    #     if ctx.obj['default']['debug'] == 'True':
    #         logger.debug(f"symbol: {symbol}")

        # return reader.parse_price_data(symbol.strip(','))
        # return reader.parse_price_data()
    # reader.parse_price_data()

    # [download(ctx, s.strip(',')) for s in ctx.obj['data_service']['symbol']]

# import requests
# headers = {
#     'Content-Type': 'application/json'
# }
# requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/aapl/prices?startDate=2019-01-02&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
# print(requestResponse.json())

# =======

# import logging

# from src.ctx_mgr import DatabaseConnectionManager


# logger = logging.getLogger(__name__)


# def get_alpha_reader_data(ctx_obj):
#     """"""
#     if ctx_obj['debug']:
#         logger.debug(f"getuse_alpha_reader_data(ctx_obj={ctx_obj})")
#     from src.data_service.reader import AlphaReader
#     reader = AlphaReader()
#     print(f"reader: {reader}")


# # def get_tiingo_data(conf_obj, ctx_obj):
# def get_tiingo_data(ctx_obj):
#     """"""
#     if ctx_obj['debug']:
#         logger.debug(f"get_tiingo_data(ctx={ctx_obj})")
#     from src.data_service.reader import TiingoReader

#     reader = TiingoReader()
#     for symbol in ctx_obj['symbol']:
#         data_list = reader.parse_price_data(symbol.strip(','))
#         _write_data_to_sqlite_db(ctx_obj, data_list)


# def _write_data_to_sqlite_db(ctx_obj, data_list):
#     """"""
#     if ctx_obj['debug']:
#         logger.debug(f"_write_data_to_sqlite_db(data_list={data_list})")

#     db_path=f"{ctx_obj['Default']['work_dir']}/{ctx_obj['Database']['db']}"

#     with DatabaseConnectionManager(db_path, mode='rw') as cursor:
#         for data in data_list:
#             cursor.execute("INSERT INTO ohlc VALUES (?,?,?,?,?,?,?);", data)
#     # for data in data_list:
#     #     print(data)
