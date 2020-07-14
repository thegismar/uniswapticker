import time
from datetime import datetime

from colorama import Back, Style
from uswapper import USwapper

us = USwapper()
sym = str.upper( input( 'symbol?' ).replace( ' ', '' ) ).split( ',' )


def currtime():
    ts = time.time()
    st = datetime.fromtimestamp( ts ).strftime( '%Y-%m-%d %H:%M:%S' )
    return st


d = {}

while True:

    out = ''
    out += Style.RESET_ALL
    for s in sym:
        if s == 'BUIDL':
            s = s.lower()

        p = float( us.getprice( symbol=s ) )
        p = us.ethprice * p

        out += f' | '
        out += Back.GREEN if p > d.get( s, 0 ) else Back.RED if p < d.get( s, 0 ) else ''
        out += f'{s}: {p:.6f}'
        out += Style.RESET_ALL

        d[s] = p
    print( f'{currtime()} {out}' )

    time.sleep( 0.5 )
