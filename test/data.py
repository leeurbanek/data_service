import datetime
from collections import namedtuple


OHLC = namedtuple('OHLC', ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'])

ctx = {
    'default': {
        'debug': 'True', 
        'temp_dir': 'temp'
    }, 
    'data_service': {
        'back_days': '5', 
        'database': 'data_service.db', 
        'frequency': 'daily', 
        'symbol': 'IWM LQD', 
        'table': 'price volume'
    }
}

read_one_price_data_IWM = [
    {
        'date': '2023-12-20T00:00:00.000Z', 
        'close': 196.28, 
        'high': 202.17, 
        'low': 196.16, 
        'open': 199.86, 
        'volume': 62360257, 
        'adjClose': 196.28, 
        'adjHigh': 202.17, 
        'adjLow': 196.16, 
        'adjOpen': 199.86, 
        'adjVolume': 62360257, 
        'divCash': 0.7339, 
        'splitFactor': 1.0
    }, 
    {
        'date': '2023-12-21T00:00:00.000Z', 
        'close': 199.62, 
        'high': 199.82, 
        'low': 197.52, 
        'open': 198.5, 
        'volume': 38613394, 
        'adjClose': 199.62, 
        'adjHigh': 199.82, 
        'adjLow': 197.52, 
        'adjOpen': 198.5, 
        'adjVolume': 38613394, 
        'divCash': 0.0, 
        'splitFactor': 1.0
    }, 
    {
        'date': '2023-12-22T00:00:00.000Z', 
        'close': 201.48, 
        'high': 202.81, 
        'low': 200.19, 
        'open': 200.88, 
        'volume': 39173804, 
        'adjClose': 201.48, 
        'adjHigh': 202.81, 
        'adjLow': 200.19, 
        'adjOpen': 200.88, 
        'adjVolume': 39173804, 
        'divCash': 0.0, 
        'splitFactor': 1.0
    }
]

parse_price_data_IWM = [
    OHLC(
        symbol='IWM', 
        date=datetime.date(2023, 12, 20), 
        open=19986, 
        high=20217, 
        low=19616, 
        close=19628, 
        volume=62360257
    ), 
    OHLC(
        symbol='IWM', 
        date=datetime.date(2023, 12, 21), 
        open=19850, 
        high=19982, 
        low=19752, 
        close=19962, 
        volume=38613394
    ), 
    OHLC(
        symbol='IWM', 
        date=datetime.date(2023, 12, 22), 
        open=20088, 
        high=20281, 
        low=20019, 
        close=20148, 
        volume=39173804
    )
]

read_one_price_data_LQD = [
    {
        'date': '2023-12-20T00:00:00.000Z', 
        'close': 110.33, 
        'high': 110.42, 
        'low': 109.905, 
        'open': 110.25, 
        'volume': 23942016, 
        'adjClose': 110.33, 
        'adjHigh': 110.42, 
        'adjLow': 109.905, 
        'adjOpen': 110.25, 
        'adjVolume': 23942016, 
        'divCash': 0.0, 
        'splitFactor': 1.0
    }, 
    {
        'date': '2023-12-21T00:00:00.000Z', 
        'close': 110.29, 
        'high': 110.71, 
        'low': 110.03, 
        'open': 110.59, 
        'volume': 24168326, 
        'adjClose': 110.29, 
        'adjHigh': 110.71, 
        'adjLow': 110.03, 
        'adjOpen': 110.59, 
        'adjVolume': 24168326, 
        'divCash': 0.0, 
        'splitFactor': 1.0
    }, 
    {
        'date': '2023-12-22T00:00:00.000Z', 
        'close': 110.1, 
        'high': 110.5, 
        'low': 109.935, 
        'open': 110.44, 
        'volume': 11037070, 
        'adjClose': 110.1, 
        'adjHigh': 110.5, 
        'adjLow': 109.935, 
        'adjOpen': 110.44, 
        'adjVolume': 11037070, 
        'divCash': 0.0, 
        'splitFactor': 1.0
    }
]

parse_price_data_LQD = [
    OHLC(
        symbol='LQD', 
        date=datetime.date(2023, 12, 20), 
        open=11025, 
        high=11042, 
        low=10990, 
        close=11033, 
        volume=23942016
    ), 
    OHLC(
        symbol='LQD', 
        date=datetime.date(2023, 12, 21), 
        open=11059, 
        high=11071, 
        low=11003, 
        close=11029, 
        volume=24168326
    ), 
    OHLC(
        symbol='LQD', 
        date=datetime.date(2023, 12, 22), 
        open=11044, 
        high=11050, 
        low=10994, 
        close=11010, 
        volume=11037070
    )
]

symbol = ['IWM', 'LQD']

close_weighted_price = {
    'default': {'debug': 'True', 'temp_dir': 'temp'}, 
    'data_service': {
        'back_days': '5', 
        'database': 'data_service.db', 
        'symbol': ['IWM', 'LQD'], 
        'table': 'price volume', 
        'url_tiingo': 'https://api.tiingo.com/tiingo', 
        'provider': 'tiingo', 
        'data_list': [
            [
                ['IWM', datetime.date(2023, 12, 19), 19774, 20055, 19728, 20018, 50840215], 
                ['IWM', datetime.date(2023, 12, 20), 19986, 20217, 19616, 19628, 62360257], 
                ['IWM', datetime.date(2023, 12, 21), 19850, 19982, 19752, 19962, 38613394], 
                ['IWM', datetime.date(2023, 12, 22), 20088, 20281, 20019, 20148, 39173804]
            ], 
            [
                ['LQD', datetime.date(2023, 12, 19), 11011, 11037, 10996, 11004, 18082571], 
                ['LQD', datetime.date(2023, 12, 20), 11025, 11042, 10990, 11033, 23942016], 
                ['LQD', datetime.date(2023, 12, 21), 11059, 11071, 11003, 11029, 24168326], 
                ['LQD', datetime.date(2023, 12, 22), 11044, 11050, 10994, 11010, 11037070]
            ]
        ]
    }
}
