# uniswapticker

very basic ticker to fetch uniswap prices from graphql API.
install requirements using pip/pip3 install -r requirements.txt

run python/python3 ticker.py [-t] [-l] [-u] symbol1 symbol2 symbol3
-l / -u are floats for the lower and upper values that trigger a pushover alarm, only works if ONE symbol is provided
-t timeout between api calls

