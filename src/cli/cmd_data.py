import logging

import click

from src.data_service import client


logger = logging.getLogger(__name__)

@click.command('data', short_help="Download historicl OHLC data", help="""
\b
NAME
""")

# @click.argument()

# @click.option()

@click.pass_context
def cli(ctx, symbol=None):
    """Run data command"""
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"cli(ctx={ctx})")
    
    if symbol:  # use symbols from command line input
        ctx.obj['data_service']['symbol'] = [
            s.upper() for s in list(symbol)
        ]
    else:  # use symbols from config file
        import re
        ctx.obj['data_service']['symbol'] = [
            s.upper() for s in re.findall(r'[^,;\s]+', ctx.obj['data_service']['symbol'])
        ]
        
    client.get_data(ctx)