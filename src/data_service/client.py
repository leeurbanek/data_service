import logging


logger = logging.getLogger(__name__)

def get_data(ctx):
    """"""
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"get_data(ctx={ctx})")

    [download(ctx, s.strip(',')) for s in ctx.obj['data_service']['symbol']]


def download(ctx, symbol):
    """"""
    debug = ctx.obj['default']['debug'] == 'True'

    if debug: logger.debug(f"download(ctx={ctx}, symbol={symbol})")
