import datetime
import logging
import sqlite3
import os

from src import config_dict


debug = config_dict['default']['debug'] == 'True'
logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Context manager for Sqlite3 databases.
    -----------------------------------------
    Commits changes on exit.\n
    Parameters
    ----------
    `db_path` : string
        Path to an Sqlite3 database (db_path='test.db' for in memory db).\n
    `mode` : string
        determines if the new database is opened read-only 'ro', read-write 'rw',\n
        read-write-create 'rwc' (mode='memory' for in-memory database.)\n
    Returns
    -------
    An Sqlite3 connection object.\n
    """
    def __init__(self, db_path=None, mode=None):
        self.db_path = db_path
        self.debug = debug
        self.mode = mode

    def __enter__(self):
        if self.debug: logger.debug('DatabaseConnectionManager.__enter__()')
        try:
            self.connection = sqlite3.connect(
                f'file:{os.path.abspath(self.db_path)}?mode={self.mode}',
                # detect_types=sqlite3.PARSE_DECLTYPES, uri=True
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, uri=True
            )
            self.cursor = self.connection.cursor()
            if self.debug: logger.debug(f"connected '{os.path.basename(self.db_path)}', mode: {self.mode}")
            # return self.cursor
            return self
        except sqlite3.Error as e:
            print(f'{e}: {self.db_path}')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.debug: logger.debug('DatabaseConnectionManager.__exit__()')
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


class DatabaseWriterManager:
    """Context manager for writing to Sqlite3 databases.
    -------------------------------------------------
    \n
    Parameters
    ----------
    \n
    Returns
    -------
    \n
    """
    def __init__(self, data=None):
        self.data = data
        self.debug = debug

    def __enter__(self):
        if self.debug: logger.debug('DatabaseWriterManager.__enter__()')
        try:
            self.output = []
            for item in self.data:
                self.output.append(item)
            if self.debug: logger.debug(self.output)
            return self
        except Exception as e:
            print(f"{e}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.debug: logger.debug('DatabaseWriterManager.__exit__()')


if __name__ == '__main__':
    import unittest

    class DatabaseConnectionManagerTest(unittest.TestCase):
        """"""
        def setUp(self) -> None:
            self.db_table = 'data'
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
                except Exception as e:
                    print(f"{e}")
                self.assertEqual(result, ('F3',))

    class DatabaseWriterManagerTest(unittest.TestCase):
        """"""
        def setUp(self) -> None:
            self.data = [
                [
                    [datetime.date(2023, 11, 27), 'EEM', 3937, 3942, 3927, 3938, 22925243], 
                    [datetime.date(2023, 11, 28), 'EEM', 3956, 3978, 3949, 3971, 35006717], 
                    [datetime.date(2023, 11, 29), 'EEM', 3951, 3972, 3944, 3948, 26049154], 
                    [datetime.date(2023, 11, 30), 'EEM', 3957, 3961, 3929, 3956, 30482770], 
                    [datetime.date(2023, 12, 1), 'EEM', 3929, 3973, 3920, 3973, 27140196]], 
                [
                    [datetime.date(2023, 11, 27), 'IWM', 17850, 17911, 17723, 17873, 30665810], 
                    [datetime.date(2023, 11, 28), 'IWM', 17855, 17922, 17720, 17804, 28350213], 
                    [datetime.date(2023, 11, 29), 'IWM', 17955, 18175, 17870, 17898, 31590200], 
                    [datetime.date(2023, 11, 30), 'IWM', 18005, 18064, 17876, 17966, 32216751], 
                    [datetime.date(2023, 12, 1), 'IWM', 17920, 18518, 17821, 18491, 64221297]], 
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
        
        def test_db_writer_mgr(self):
            with DatabaseWriterManager(data=self.data) as writer:
                writer.output

    unittest.main(verbosity=2)


# =======

# import logging
# import os.path
# from configparser import ConfigParser

# import click

# from src import config_file, conf_obj, _value
# from src.ctx_mgr import DatabaseConnectionManager
# from src.data_service import client

# conf_obj.read(config_file)

# logger = logging.getLogger(__name__)


# def _add_database_table(db_con, table_name):
#     """
#     ----------
#     `ctx_obj` : dictionary
#         Python Click context object.\n
#     `db_con` : sqlite3.Connection object
#         Connection to the time series database.\n
#     """
#     db_con.execute(f'''
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             DateDATENOT NULL,
#             High     INTEGER  NOT NULL,
#             Low      INTEGER  NOT NULL,
#             Close    INTEGER  NOT NULL,
#             AdjCl    INTEGER  NOT NULL,
#             Volume   INTEGER  NOT NULL,
#             PRIMARYKEY(Date));
#         ''')


# def _add_ohlc_table(conf_obj, ctx_obj, db_con):
#     """Create the Open, High, Low, Close, AdjCl, Volume table.
#     --------------------------------------------------------
#     Fields are Date, Symbol, Open, High, Low, Close, Volume.\n
#     Parameters
#     ----------
#     `ctx_obj` : dictionary
#         Python Click context object.\n
#     `db_con` : sqlite3.Connection object
#         Connection to the time series database.\n
#     """
#     if ctx_obj['debug']:
#         logger.debug(f"_add_ohlc_table(db_con={db_con})")

#     db_table = 'ohlc' if _value(ctx_obj['Default']['db_table']) is None else ctx_obj['Default']['db_table']
#     db_con.execute(f'''
#         CREATE TABLE IF NOT EXISTS {db_table} (
#             Date    DATE        NOT NULL,
#             Symbol  TEXT        NOT NULL,
#             Open    INTEGER     NOT NULL,
#             High    INTEGER     NOT NULL,
#             Low     INTEGER     NOT NULL,
#             Close   INTEGER     NOT NULL,
#             Volume  INTEGER     NOT NULL,
#             PRIMARY KEY (Date, Symbol));
#         ''')


# @click.command('data', short_help="Fetch online OHLC price and volume data", help="""
# \b
# NAME
#     data -- Retrieve OHLC data from various online sources
# \b
# SYNOPSIS
#     data [Options] [ticker1 ticker2 ticker3 ...]
# \b
# DESCRIPTION
#     The data utility attempts to retrieve OHLC data from various
#     online sources.  If no ticker symbols are provided the default
#     symbols from the config settings are used.
#     Try 'markdata-cli config --help' for help with config settings.
# """)

# @click.argument('symbol', nargs=-1, default=None, required=False, type=str)

# @click.option('--alpha', 'opt_trans', flag_value='alpha', help='Fetch data from https://www.alphavantage.co/')
# @click.option('--tiingo', 'opt_trans', flag_value='tiingo', help='Fetch data from https://api.tiingo.com/')

# @click.pass_context
# def cli(ctx, opt_trans, symbol):
#     """Run chart command"""
#     if ctx.obj['debug']:
#         logger.debug(f"cli(ctx, opt_trans={opt_trans}, symbol={symbol })")

#     if opt_trans:
#         # check if defaults are set
#         if ctx.obj['Default']['work_dir'] == 'None':
#             click.echo("Error: Work directory not set\nTry 'markdata config --help' for help.")
#             return
#         if ctx.obj['Database']['db'] == 'None':
#             click.echo("Error: The database name is not set\nTry 'markdata config --help' for help.")
#             return
#         # create database and add talbe if not exist
#         db_path = f"{ctx.obj['Default']['work_dir']}/{ctx.obj['Database']['db']}"
#         if not os.path.isfile(db_path):
#             with DatabaseConnectionManager(db_path=db_path, mode='rwc') as db_con:
#                 _add_ohlc_table(conf_obj=ctx.obj, ctx_obj=ctx.obj, db_con=db_con)

#         if symbol:  # use symbols from command line input
#             symbol = [s.upper() for s in list(symbol)]
#         else:  # use symbols from config.ini
#             symbol = conf_obj.getlist('Ticker', 'symbol')

#         # add parameters to context object
#         ctx.obj['opt_trans'] = opt_trans
#         ctx.obj['symbol'] = symbol

#         # select data provider
#         if opt_trans == 'alpha':
#             client.get_alpha_data(ctx)
#         elif opt_trans == 'tiingo':
#             # client.get_tiingo_data(conf_obj=conf_obj, ctx_obj=ctx.obj)
#             client.get_tiingo_data(ctx)

#     else:  # print default message
#         click.echo(f"""Usage: markdata data [OPTIONS] [SYMBOL]...
# Try 'markdata data --help' for help.""")

# # subprocess.run(['open', filename], check=True)

# # =======

# # eem = [{'date': '2023-03-09T00:00:00.000Z', 'close': 38.04, 'high': 38.58, 'low': 37.96, 'open': 38.51, 'volume': 40118857, 'adjClose': 38.04, 'adjHigh': 38.58, 'adjLow': 37.96, 'adjOpen': 38.51, 'adjVolume': 40118857, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2023-03-10T00:00:00.000Z', 'close': 37.84, 'high': 38.25, 'low': 37.8, 'open': 38.02, 'volume': 49316671, 'adjClose': 37.84, 'adjHigh': 38.25, 'adjLow': 37.8, 'adjOpen': 38.02, 'adjVolume': 49316671, 'divCash': 0.0, 'splitFactor': 1.0}]
# # iwm = [{'date': '2023-03-09T00:00:00.000Z', 'close': 181.41, 'high': 187.27, 'low': 181.28, 'open': 186.73, 'volume': 33546890, 'adjClose': 181.41, 'adjHigh': 187.27, 'adjLow': 181.28, 'adjOpen': 186.73, 'adjVolume': 33546890, 'divCash': 0.0, 'splitFactor': 1.0}, {'date': '2023-03-10T00:00:00.000Z', 'close': 176.18, 'high': 180.39, 'low': 174.255, 'open': 180.39, 'volume': 67388021, 'adjClose': 176.18, 'adjHigh': 180.39, 'adjLow': 174.255, 'adjOpen': 180.39, 'adjVolume': 67388021, 'divCash': 0.0, 'splitFactor': 1.0}]

# # =======

# # connector.execute("insert into DATAGERMANY values (NULL,?,?,?,?,?)", *row)

# # =======

# # import datetime
# # import sqlite3

# # # get the current datetime and store it in a variable
# # currentDateTime = datetime.datetime.now()

# # # make the database connection with detect_types
# # connection = sqlite3.connect(
# #     'StudentAssignment.db',
# #     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
# # )
# # cursor = connection.cursor()

# # # create table in database
# # createTable = '''CREATE TABLE ASSIGNMENT (
# # 	StudentId INTEGER,
# # 	StudentName VARCHAR(100),
# # 	SubmissionDate TIMESTAMP);'''
# # cursor.execute(createTable)

# # # create query to insert the data
# # insertQuery = """INSERT INTO ASSIGNMENT
# # 	VALUES (?, ?, ?);"""

# # # insert the data into table
# # cursor.execute(insertQuery, (1, "Virat Kohli",
# # 							currentDateTime))
# # cursor.execute(insertQuery, (2, "Rohit Pathak",
# # 							currentDateTime))
# # print("Data Inserted Successfully !")

# # # commit the changes,
# # # close the cursor and database connection
# # connection.commit()
# # cursor.close()
# # connection.close()

# # =======

# # import datetime
# # import sqlite3

# # make a database connection and cursor object
# # connection = sqlite3.connect(
# #     'StudentAssignment.db',
# #     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
# # )
# # cursor = connection.cursor()

# # # select query to retrieve data
# # cursor.execute("SELECT * from ASSIGNMENT where StudentId = 2")
# # fetchedData = cursor.fetchall()

# # # to access specific fetched data
# # for row in fetchedData:
# # 	StudentID = row[0]
# # 	StudentName = row[1]
# # 	SubmissionDate = row[2]
# # 	print(StudentName, ", ID -",
# # 		StudentID, "Submitted Assignments")
# # 	print("Date and Time : ",
# # 		SubmissionDate)
# # 	print("Submission date type is",
# # 		type(SubmissionDate))

# # # commit the changes,
# # # close the cursor and database connection
# # cursor.close()
# # connection.close()
