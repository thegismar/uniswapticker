import time
from datetime import datetime

from uswap import USwapper

us = USwapper()
sym = str.upper( input( 'symbol?' ).replace( ' ', '' ) ).split( ',' )


def currtime():
    ts = time.time()
    st = datetime.fromtimestamp( ts ).strftime( '%Y-%m-%d %H:%M:%S' )
    return st


while True:

    out = ''
    for s in sym:
        p = float( us.getprice( symbol=s ) )
        p = us.ethprice * p
        out += f' | {s}: {p:.6f}'

    print( f'{currtime()} {out}' )

    time.sleep( 1 )
