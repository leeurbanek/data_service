import logging
import sqlite3
import os

from src import config_dict


debug = config_dict['default']['debug'] == 'True'
logger = logging.getLogger(__name__)


class DatabaseWriter:
    """"""
    def __init__(self, ctx):
        self.db_path = f"{ctx.obj['default']['temp_dir']}/{ctx.obj['data_service']['database']}"
        self.debug = f"{ctx.obj['default']['debug']}" == 'True'
        if self.debug: logger.debug(self)


def create_database(ctx):
    """"""
    if debug: logger.debug(f"create_database(ctx={ctx})")

    db_path = f"{ctx.obj['default']['temp_dir']}/{ctx.obj['data_service']['database']}"

    import re
    with DatabaseConnectionManager(db_path=db_path, mode='rwc') as db:
        table_list = [t.lower() for t in re.findall(r'[^,;\s]+', ctx.obj['data_service']['table'])]
        for table in table_list:
            db.cursor.execute(f'''
                CREATE TABLE {table} (
                    Date    INTEGER    NOT NULL, 
                    PRIMARY KEY (Date)
                )
            ''')
            # add symbol column to table
            col_list = ctx.obj['data_service']['symbol']
            for col in col_list:
                db.cursor.execute(f'''
                    ALTER TABLE {table} ADD COLUMN {col} INTEGER
                ''')
    if not debug: print(f"created database: {db_path}")


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


# def close_weighted_price(ctx):
#     """"""
#     if ctx.obj['default']['debug'] == 'True':
#         logger.debug(f"close_weighted_price(ctx={ctx.obj})")


# class PriceManager:
#     """Context manager for writing to Sqlite3 databases.
#     -------------------------------------------------
#     \n
#     Parameters
#     ----------
#     \n
#     Returns
#     -------
#     \n
#     """
#     def __init__(self, data=None):
#         self.data = data
#         self.debug = debug

#     def __enter__(self):
#         if self.debug: logger.debug('PriceManager.__enter__()')
#         try:
#             self.column = []  # symbol
#             for item in self.data:
#                 self.column.append(item[0][1])

#             self.index = []  # date
#             for item in self.data[0]:
#                 self.index.append(item[0])

#             self.price = []  # close weighted price
#             for item in self.data:
#                 self.price.append([
#                     round(  # high + low + close
#                         (i[3] + i[4] + i[5]*2) / 4
#                     )for i in item
#                 ])

#             if self.debug: logger.debug(
#                 f"column={self.column}, "
#                 f"index={self.index}, "
#                 f"price={self.price}"
#             )
#             return self

#         except Exception as e:
#             print(f"{e}")

#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         if self.debug: logger.debug('PriceManager.__exit__()')


# class VolumeManager:
#     """"""
#     pass

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
