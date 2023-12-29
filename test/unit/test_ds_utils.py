import datetime
import logging
import sqlite3
import os
import unittest
from unittest.mock import Mock

# from test.data import (get_data)
from src import config_dict
from src.data_service.utils_sqlite import DatabaseConnectionManager
# from src.data_service.utils import PriceManager


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

# class PriceManagerTest(unittest.TestCase):
#     """"""
#     def setUp(self) -> None:
#         self.data = get_data

#     def tearDown(self) -> None:
#         logging.disable(logging.CRITICAL)
#         del self.data
    
#     def test_column_index_price_value(self):
#         with PriceManager(data=self.data) as writer:
#             self.assertEqual(['IWM', 'LQD'], writer.column)
#             self.assertEqual([
#                 datetime.date(2023, 12, 11), 
#                 datetime.date(2023, 12, 12), 
#                 datetime.date(2023, 12, 13), 
#                 datetime.date(2023, 12, 14), 
#                 datetime.date(2023, 12, 15)
#             ], writer.index)
#             self.assertEqual([
#                 [18697, 18675, 19149, 19848, 19740], 
#                 [10682, 10737, 10901, 11050, 11036]
#             ], writer.price)


if __name__ == '__main__':
    unittest.main(verbosity=2)
