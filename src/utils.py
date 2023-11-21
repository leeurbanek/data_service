import logging
import sqlite3
import os

from src import config_dict



logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Context manager for Sqlite3 databases.
    -----------------------------------------
    Commits changes on exit.\n
    Parameters
    ----------
    `db_path` : string
        Path to an Sqlite3 database (default='test.db' for in memory db).\n
    `mode` : string
        determines if the new database is opened read-only 'ro', read-write 'rw',\n
        read-write-create 'rwc', or pure in-memory database 'memory' (default) mode.\n
    Returns
    -------
    An Sqlite3 connection object.\n
    """
    def __init__(self, db_path='test.db', mode='memory'):
        self.db_path = db_path
        self.mode = mode

    def __enter__(self):
        logger.debug('DatabaseConnectionManager.__enter__()')
        try:
            self.connection = sqlite3.connect(
                f'file:{os.path.abspath(self.db_path)}?mode={self.mode}',
                # detect_types=sqlite3.PARSE_DECLTYPES, uri=True
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, uri=True
            )
            self.cursor = self.connection.cursor()
            logger.debug(f"connected '{os.path.basename(self.db_path)}', mode: {self.mode}")
            # return self.cursor
            return self
        except sqlite3.Error as e:
            print(f'{e}: {self.db_path}')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.debug('DatabaseConnectionManager.__exit__()')
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    import unittest

    class ContextManagerTest(unittest.TestCase):
        def setUp(self) -> None:
            self.db_table = 'data'
            self.rows = [
                ('D1','F1'), ('D2','F2'), ('D3','F3'),
            ]

        def test_db_ctx_mgr_in_memory_mode(self):
            with DatabaseConnectionManager() as db:
                db.cursor.execute(f'''
                    CREATE TABLE {self.db_table} (
                        Date    DATE        NOT NULL,
                        Field   INTEGER     NOT NULL,
                        PRIMARY KEY (Date)
                    );
                ''')
                db.cursor.executemany(f'INSERT INTO {self.db_table} VALUES (?,?)', self.rows)
                try:
                    sql = db.cursor.execute(f"SELECT Field FROM {self.db_table} WHERE ROWID IN (SELECT max(ROWID) FROM {self.db_table});")
                    result = sql.fetchone()
                except Exception as e:
                    print(f"{e}")
                self.assertEqual(result, ('F3',))

    unittest.main()
