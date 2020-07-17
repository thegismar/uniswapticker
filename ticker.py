import argparse
import time
from datetime import datetime

from colorama import Back, Style
from uswapper import USwapper

parser = argparse.ArgumentParser()
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


d = {}

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

        out += f' | '
        out += f'{s}: '
        out += Back.GREEN if pusd > d.get( s, 0 ) else Back.RED if pusd < d.get( s, 0 ) else ''
        out += f'{pusd:.6f}$ {peth:.8f}Ξ'
        out += Style.RESET_ALL

        d[s] = pusd
    print( f'{currtime()} {out}' )

    time.sleep( 0.5 )
