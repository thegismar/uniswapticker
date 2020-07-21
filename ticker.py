import argparse
import os
import time
from datetime import datetime
from colorama import Back, Style
from pushover import Client
from uswapper import USwapper

parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store', help='lower threshold for pushover alarm, need '
                                               'environment variable PUSHOVER_KEY and PUSHOVER_TOKEN', required=False)
parser.add_argument('-u', action='store', help='upper threshold for pushover alarm, need'
                                               'environment variable PUSHOVER_KEY and PUSHOVER_TOKEN', required=False)
parser.add_argument( 'symbol', nargs='+' )

args = parser.parse_args()

_ = ''

for a in args.symbol:
    _ += f'{a} '

us = USwapper()
sym = str.upper( _ ).split( ' ' )


def currtime():
    ts = time.time()
    st = datetime.fromtimestamp( ts ).strftime( '%Y-%m-%d %H:%M:%S' )
    return st


p_key = os.getenv( 'PUSHOVER_KEY' )
p_token = os.getenv( 'PUSHOVER_TOKEN' )

client = Client( p_key, api_token=p_token )

d = {}
last_push = None

while True:

    out = ''
    out += Style.RESET_ALL

    for s in args.symbol:
        s = s.upper()

        if s == 'BUIDL':
            s = s.lower()

        peth = float( us.getprice( symbol=s ) )
        pusdc = float( us.getprice( symbol='USDC' ) )
        pusd = peth / pusdc

        if (args.l and args.u) is not None:
            if pusd < float(args.l) and (last_push is None or (time.time() - last_push) > 900):
                client.send_message( f'{s} is at {pusd:.2f}', title=f'{s} crashing!!', priority=2, expire=120, retry=60,
                                     sound='persistent' )
                last_push = time.time()

            if pusd > float(args.u) and (last_push is None or (time.time() - last_push) > 900):
                client.send_message( f'{s} is at {pusd:.2f}', title=f'{s} rocketing!!', priority=2, expire=120, retry=60,
                                     sound='persistent' )
                last_push = time.time()

        out += f' | '
        out += f'{s}: '
        out += Back.GREEN if peth > d.get( s, 0 ) else Back.RED if peth < d.get( s, 0 ) else ''
        out += f'{pusd:.6f}$ {peth:.8f}Ξ'
        out += Style.RESET_ALL

        d[s] = peth

        print( f'{currtime()} {out}' )
