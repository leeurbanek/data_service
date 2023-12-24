import datetime


ctx_tiingo = {
    'default': {'debug': 'True', 'temp_dir': 'temp'}, 
    'data_service': {'back_days': '5', 'database': 'data_service.db', 'symbol': 'IWM LQD', 'url_tiingo': 'https://api.tiingo.com/tiingo'}
}

read_one_price_data_IWM = [
    {'date': '2023-12-11T00:00:00.000Z', 'close': 187.19, 'high': 187.62, 'low': 185.885, 'open': 186.68, 'volume': 29302064, 'adjClose': 187.19, 'adjHigh': 187.62, 'adjLow': 185.885, 'adjOpen': 186.68, 'adjVolume': 29302064, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-12T00:00:00.000Z', 'close': 187.0, 'high': 187.655, 'low': 185.335, 'open': 186.97, 'volume': 32023999, 'adjClose': 187.0, 'adjHigh': 187.655, 'adjLow': 185.335, 'adjOpen': 186.97, 'adjVolume': 32023999, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-13T00:00:00.000Z', 'close': 193.33, 'high': 193.64, 'low': 185.67, 'open': 187.1, 'volume': 69484819, 'adjClose': 193.33, 'adjHigh': 193.64, 'adjLow': 185.67, 'adjOpen': 187.1, 'adjVolume': 69484819, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-14T00:00:00.000Z', 'close': 198.71, 'high': 200.035, 'low': 196.48, 'open': 196.87, 'volume': 83649334, 'adjClose': 198.71, 'adjHigh': 200.035, 'adjLow': 196.48, 'adjOpen': 196.87, 'adjVolume': 83649334, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-15T00:00:00.000Z', 'close': 197.04, 'high': 199.55, 'low': 195.95, 'open': 198.95, 'volume': 74160699, 'adjClose': 197.04, 'adjHigh': 199.55, 'adjLow': 195.95, 'adjOpen': 198.95, 'adjVolume': 74160699, 'divCash': 0.0, 'splitFactor': 1.0}
]

parse_price_data_IWM = [
    [datetime.date(2023, 12, 11), 'IWM', 18668, 18762, 18588, 18719, 29302064], 
    [datetime.date(2023, 12, 12), 'IWM', 18697, 18766, 18534, 18700, 32023999], 
    [datetime.date(2023, 12, 13), 'IWM', 18710, 19364, 18567, 19333, 69484819], 
    [datetime.date(2023, 12, 14), 'IWM', 19687, 20004, 19648, 19871, 83649334], 
    [datetime.date(2023, 12, 15), 'IWM', 19895, 19955, 19595, 19704, 74160699]
]

read_one_price_data_LQD = [
    {'date': '2023-12-11T00:00:00.000Z', 'close': 107.33, 'high': 107.36, 'low': 106.78, 'open': 107.22, 'volume': 17714571, 'adjClose': 106.9499753455, 'adjHigh': 106.9798691241, 'adjLow': 106.4019227373, 'adjOpen': 106.8403648238, 'adjVolume': 17714571, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-12T00:00:00.000Z', 'close': 107.94, 'high': 107.9758, 'low': 107.14, 'open': 107.32, 'volume': 22111087, 'adjClose': 107.557815511, 'adjHigh': 107.5934887535, 'adjLow': 106.7606480808, 'adjOpen': 106.9400107526, 'adjVolume': 22111087, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-13T00:00:00.000Z', 'close': 109.75, 'high': 109.945, 'low': 108.13, 'open': 108.35, 'volume': 33623567, 'adjClose': 109.3614068216, 'adjHigh': 109.5557163827, 'adjLow': 107.7471427756, 'adjOpen': 107.9663638189, 'adjVolume': 33623567, 'divCash': 0.0, 'splitFactor': 1.0}, 
    {'date': '2023-12-14T00:00:00.000Z', 'close': 110.52, 'high': 110.865, 'low': 110.12, 'open': 110.24, 'volume': 28202255, 'adjClose': 110.52, 'adjHigh': 110.865, 'adjLow': 110.12, 'adjOpen': 110.24, 'adjVolume': 28202255, 'divCash': 0.39271, 'splitFactor': 1.0}, 
    {'date': '2023-12-15T00:00:00.000Z', 'close': 110.36, 'high': 110.57, 'low': 110.14, 'open': 110.42, 'volume': 17904113, 'adjClose': 110.36, 'adjHigh': 110.57, 'adjLow': 110.14, 'adjOpen': 110.42, 'adjVolume': 17904113, 'divCash': 0.0, 'splitFactor': 1.0}
]

parse_price_data_LQD = [
    [datetime.date(2023, 12, 11), 'LQD', 10684, 10698, 10640, 10695, 17714571], 
    [datetime.date(2023, 12, 12), 'LQD', 10694, 10759, 10676, 10756, 22111087], 
    [datetime.date(2023, 12, 13), 'LQD', 10797, 10956, 10775, 10936, 33623567], 
    [datetime.date(2023, 12, 14), 'LQD', 11024, 11086, 11012, 11052, 28202255], 
    [datetime.date(2023, 12, 15), 'LQD', 11042, 11057, 11014, 11036, 17904113]
]

get_data = [
    [
        [datetime.date(2023, 12, 11), 'IWM', 18668, 18762, 18588, 18719, 29302064], 
        [datetime.date(2023, 12, 12), 'IWM', 18697, 18766, 18534, 18700, 32023999], 
        [datetime.date(2023, 12, 13), 'IWM', 18710, 19364, 18567, 19333, 69484819], 
        [datetime.date(2023, 12, 14), 'IWM', 19687, 20004, 19648, 19871, 83649334], 
        [datetime.date(2023, 12, 15), 'IWM', 19895, 19955, 19595, 19704, 74160699]
    ], 
    [
        [datetime.date(2023, 12, 11), 'LQD', 10684, 10698, 10640, 10695, 17714571], 
        [datetime.date(2023, 12, 12), 'LQD', 10694, 10759, 10676, 10756, 22111087], 
        [datetime.date(2023, 12, 13), 'LQD', 10797, 10956, 10775, 10936, 33623567], 
        [datetime.date(2023, 12, 14), 'LQD', 11024, 11086, 11012, 11052, 28202255], 
        [datetime.date(2023, 12, 15), 'LQD', 11042, 11057, 11014, 11036, 17904113]
    ]
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
