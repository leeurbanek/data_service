import datetime
import logging
import sqlite3
import os
import unittest
from unittest.mock import Mock

from src import config_dict
from src.data_service.utils import DatabaseConnectionManager
from src.data_service.utils import PriceManager


debug = config_dict['default']['debug'] == 'True'
logger = logging.getLogger(__name__)


class DatabaseConnectionManagerTest(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.db_table = 'data'
        self.debug = debug
        self.rows = [
            ('D1','F1'), ('D2','F2'), ('D3','F3'),
        ]

    def tearDown(self) -> None:
    #    logging.disable(logging.CRITICAL)
        del self.db_table, self.rows
    
    def test_db_ctx_mgr_in_memory_mode(self):
        with DatabaseConnectionManager(db_path='test_db', mode='memory') as db:
            db.cursor.execute(f'''
                CREATE TABLE {self.db_table} (
                    Date    DATE        NOT NULL,
                    Field   INTEGER     NOT NULL,
                    PRIMARY KEY (Date)
                );
            ''')
            db.cursor.executemany(f'''
                INSERT INTO {self.db_table} VALUES (?,?)
                ''', self.rows)
            try:
                sql = db.cursor.execute(f'''
                    SELECT Field FROM {self.db_table} 
                    WHERE ROWID IN (SELECT max(ROWID) 
                    FROM {self.db_table});
                    ''')
                result = sql.fetchone()
                if self.debug: logger.debug(f"result={result}")
            except Exception as e:
                print(f"{e}")
            self.assertEqual(result, ('F3',))

class PriceManagerTest(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.data = [
            [
                [datetime.date(2023, 11, 27), 'EEM', 3937, 3942, 3927, 3938, 22925243], 
                [datetime.date(2023, 11, 28), 'EEM', 3956, 3978, 3949, 3971, 35006717], 
                [datetime.date(2023, 11, 29), 'EEM', 3951, 3972, 3944, 3948, 26049154], 
                [datetime.date(2023, 11, 30), 'EEM', 3957, 3961, 3929, 3956, 30482770], 
                [datetime.date(2023, 12, 1), 'EEM', 3929, 3973, 3920, 3973, 27140196]
            ], 
            [
                [datetime.date(2023, 11, 27), 'IWM', 17850, 17911, 17723, 17873, 30665810], 
                [datetime.date(2023, 11, 28), 'IWM', 17855, 17922, 17720, 17804, 28350213], 
                [datetime.date(2023, 11, 29), 'IWM', 17955, 18175, 17870, 17898, 31590200], 
                [datetime.date(2023, 11, 30), 'IWM', 18005, 18064, 17876, 17966, 32216751], 
                [datetime.date(2023, 12, 1), 'IWM', 17920, 18518, 17821, 18491, 64221297]
            ], 
            [
                [datetime.date(2023, 11, 27), 'LQD', 10467, 10520, 10449, 10518, 17919475], 
                [datetime.date(2023, 11, 28), 'LQD', 10500, 10564, 10490, 10560, 21320767], 
                [datetime.date(2023, 11, 29), 'LQD', 10615, 10652, 10601, 10646, 20661847], 
                [datetime.date(2023, 11, 30), 'LQD', 10622, 10625, 10569, 10590, 41950881], 
                [datetime.date(2023, 12, 1), 'LQD', 10604, 10722, 10590, 10717, 27733665]
            ]
        ]

    def tearDown(self) -> None:
        logging.disable(logging.CRITICAL)
        del self.data
    
    def test_column_index_price_value(self):
        with PriceManager(data=self.data) as writer:
            self.assertEqual(['EEM', 'IWM', 'LQD'], writer.column)
            self.assertEqual([datetime.date(2023, 11, 27), datetime.date(2023, 11, 28), datetime.date(2023, 11, 29), datetime.date(2023, 11, 30), datetime.date(2023, 12, 1)], writer.index)
            self.assertEqual([[3936, 3967, 3953, 3950, 3960], [17845, 17812, 17960, 17968, 18330], [10501, 10544, 10636, 10594, 10686]], writer.price)


if __name__ == '__main__':
    unittest.main(verbosity=2)
