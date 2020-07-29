# uniswapticker

very basic ticker to fetch uniswap prices from graphql API.

installation
-----------------------

install requirements using pip/pip3 install -r requirements.txt

usage
-----------------------

run python/python3 ticker.py [-t] [-l] [-u] symbol1 symbol2 symbol3

flags
-----------------------

-t float for timeout between calls

pushover account needed
-----------------------
-l float below which pushover message will be triggered
-u float above which pushover message will be triggered

PUSHOVER_KEY & PUSHOVER_TOKEN must be environment variables

current limitations
-----------------------
pushover alarms can only
color changes based on ETH value, not USDC
