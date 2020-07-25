import argparse
import os
import sys
import time
from datetime import datetime

from colorama import Back, Style
from pushover import Client
from uswapper import USwapper

# get cmd line args
parser = argparse.ArgumentParser()
parser.add_argument( '-l', action='store', help='lower threshold for pushover alarm, need '
                                                'environment variable PUSHOVER_KEY and PUSHOVER_TOKEN'
                                                'THIS WILL NOT WORK WITH MULTIPE TOKENS', required=False )
parser.add_argument( '-u', action='store', help='upper threshold for pushover alarm, need'
                                                'environment variable PUSHOVER_KEY and PUSHOVER_TOKEN'
                                                'THIS WILL NOT WORK WITH MULTIPLE TOKENS', required=False )
parser.add_argument( '-t', action='store', help='timeout between api calls, increase this if receiving HTTP errors, '
                                                'default is 0', required=False, default=0 )
parser.add_argument( 'symbol', nargs='+', help='list of symbols for ticker separated by space' )
args = parser.parse_args()

# check if lower/upper alerts are given with multiple symbols
# if not get env variables and initiate pushover client

alerts = False if (args.l or args.u) and len( args.symbol ) > 1 else False if (args.l and args.u) and len(
        args.symbol ) == 1 else None

if alerts is False:
    parser.error( 'pushover alerts only implemented for ONE token' )
elif alerts is True:
    try:
        p_key = os.getenv( 'PUSHOVER_KEY' )
        p_token = os.getenv( 'PUSHOVER_TOKEN' )
    except KeyError:
        print( 'Environment variables for pushover not set' )  # pushover client init
        sys.exit( 1 )
    else:
        client = Client( p_key, api_token=p_token )
        last_push = None

# adding cmd ine tokens to string
_ = ''
for a in args.symbol:
    _ += f'{a} '
sym = str.upper( _ ).split( ' ' )


# current time output
def currtime():
    ts = time.time()
    st = datetime.fromtimestamp( ts ).strftime( '%Y-%m-%d %H:%M:%S' )
    return st


# init uswapper client that takes care of the api calls
us = USwapper()

# dictionary to store previous values and compare current ones
d = {}

while True:

    out = ''
    out += Style.RESET_ALL

    for s in args.symbol:

        s = s.upper()

        # since buidl uppercase is buidl v1 according to uniswap
        if s == 'BUIDL':
            s = s.lower()

        try:
            us.isuniswapasset( s )
        except KeyError:
            print( f'Silly Normie, {s} is not part of Uniswap tokens!! Go back to Binance.' )
            sys.exit()

        peth = float( us.getprice( symbol=s ) )
        pusdc = float( us.getprice( symbol='USDC' ) )
        pusd = peth / pusdc

        if alerts:
            if pusd < float( args.l ) and (last_push is None or (time.time() - last_push) > 900):
                client.send_message( f'{s} is at {pusd:.2f}', title=f'{s} crashing!!', priority=2, expire=120, retry=60,
                                     sound='persistent' )
                last_push = time.time()

            if pusd > float( args.u ) and (last_push is None or (time.time() - last_push) > 900):
                client.send_message( f'{s} is at {pusd:.2f}', title=f'{s} rocketing!!', priority=2, expire=120,
                                     retry=60, sound='persistent' )
                last_push = time.time()

        out += f' | '
        out += f'{s}: '
        out += Back.GREEN if peth > d.get( f'{s}eth', 0 ) else Back.RED if peth < d.get( f'{s}eth', 0 ) else ''
        out += f'{pusd:.6f}$'
        out += '   '
        out += f'{peth:.8f}Ξ'
        out += Style.RESET_ALL

        d[f'{s}eth'] = peth
        d[f'{s}usd'] = pusd

    print( f'{currtime()} {out}' )
    time.sleep( int( args.t ) )
