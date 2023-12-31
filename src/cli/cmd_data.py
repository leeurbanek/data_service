import logging
import os

import click

from src.data_service import client
from src.data_service.utils import sqlite_create_database
# from src.data_service.utils import close_weighted_price


logger = logging.getLogger(__name__)

@click.command('data', short_help="Download historicl OHLC data", help="""
\b
NAME
    data -- Retrieve OHLC data from various online sources
\b
SYNOPSIS
    data [Options] [ticker1 ticker2 ticker3 ...]
\b
DESCRIPTION
    The data utility attempts to retrieve OHLC data from various
    online sources.  If no ticker symbols are provided the default
    symbols from the config settings are used.
    Try 'markdata-cli config --help' for help with config settings.
""")

@click.argument('symbol', nargs=-1, default=None, required=False, type=str)

@click.option('--alpha', 'opt_trans', flag_value='alpha', help='Fetch data from https://www.alphavantage.co/')
@click.option('--tiingo', 'opt_trans', flag_value='tiingo', help='Fetch data from https://api.tiingo.com/')

@click.pass_context
def cli(ctx, opt_trans=None, symbol=None):
    """Run data command"""
    if ctx.obj['default']['debug'] == 'True': logger.debug(f"cli(ctx={ctx.obj})")

    if opt_trans:    
        ctx.obj['data_service']['provider'] = opt_trans

        if symbol:  # use symbols from command line input
            ctx.obj['data_service']['symbol'] = [
                s.upper() for s in list(symbol)
            ]
        else:  # use symbols from cfg_data.ini file
            import re  # remove commas, etc.
            ctx.obj['data_service']['symbol'] = [  # convert str to list
                s.upper() for s in re.findall(r'[^,;\s]+', ctx.obj['data_service']['symbol'])
            ]
        # check database exists if not create it
        if not os.path.isfile(f"{ctx.obj['default']['temp_dir']}/{ctx.obj['data_service']['database']}"):
            sqlite_create_database(ctx)
            if ctx.obj['default']['debug'] == 'True':
                logger.debug(f"create database: {ctx.obj['default']['temp_dir']}/{ctx.obj['data_service']['database']}\n")

        client.get_data(ctx)

    else:  # print default message
        click.echo(f"""Usage: dataserv-cli data [OPTIONS] [SYMBOL]...
You must specify a data provider option.
Try 'dataserv-cli data --help' for help.""")
