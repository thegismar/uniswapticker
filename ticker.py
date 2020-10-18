import argparse
import os
import sys
import time
from datetime import datetime
from colorama import Back, Style
from uswapper import USwapper

# get cmd line args
parser = argparse.ArgumentParser()
parser.add_argument('symbol', nargs='+', help='list of symbols for ticker separated by space')
args = parser.parse_args()


# current time output
def currtime():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st


# init uswapper client that takes care of the api calls
us = USwapper()

# dictionary to store previous values and compare current ones
d = {}

symbols = ["USDC"]
for s in args.symbol:

    if str.startswith(s, '0x'):
        s = str.lower(s)
    else:
        s = str.upper(s)

    try:
        us.isuniswapasset(s)
    except KeyError:
        print(f'Silly Normie, {s} is not part of Uniswap tokens!! Go back to Binance.')
        sys.exit()

    symbols.append(s)

while True:

    prices = us.getprice(symbols)

    out = ''
    out += Style.RESET_ALL

    for i in prices:
        peth = float(prices[i])
        pusd = float(peth) / float(prices['USDC'])

        if i == 'USDC':
            continue

        out += f' | '
        out += f'{i}: '
        out += Back.GREEN if peth > d.get(f'{i}eth', 0) else Back.RED if peth < d.get(f'{i}eth',
                                                                                      0) else ''
        out += f'{pusd:.6f}$'
        out += '   '
        out += f'{peth:.8f}Ξ'
        out += Style.RESET_ALL

        d[f'{i}eth'] = peth
        d[f'{i}usd'] = pusd

    print(f'{currtime()} {out}')
