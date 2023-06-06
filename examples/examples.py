from coinpaprika.client import Client

#
# FREE CLIENT
#

free_client = Client()

# List coins
free_client.coins()

# Get coin by ID (example: btc-bitcoin)
free_client.coin("btc-bitcoin")

# Get tweets by coin ID (max 50 tweets)
free_client.twitter("btc-bitcoin")

# Get coin events by coin ID
free_client.events("btc-bitcoin")

# Get exchanges by coin ID
free_client.exchanges("btc-bitcoin")

# Get markets by coin ID (USD,BTC,ETH,PLN)
free_client.markets("btc-bitcoin", quotes="USD")

# Get 24h OHLC candle (USD,BTC)
free_client.candle("btc-bitcoin")

# Get today OHLC (can change every each request until actual close of the day at 23:59:59)
free_client.today("btc-bitcoin")

# Get people by ID (example: vitalik-buterin)
free_client.people("vitalik-buterin")

# List tags
free_client.tags()

free_client.tags(additional_fields="coins,icos")

# Get tag by ID
free_client.tag("blockchain-service")

# Get tickers for all coins (USD,BTC,ETH)
free_client.tickers()

# Get ticker information for a specific coin (USD,BTC,ETH)
free_client.ticker("btc-bitcoin")

# List exchanges
free_client.exchange_list()

# Get exchange by ID
free_client.exchange("binance", quotes="USD")

# Get markets by exchange ID (USD,BTC,ETH,PLN) with quotes USD
free_client.exchange_markets("binance", quotes="USD")

# Search
free_client.search(q="btc", c="currencies,exchanges,icos,people,tags", modifier="symbol_search", limit=42)

# Price converter
free_client.price_converter(base_currency_id="btc-bitcoin", quote_currency_id="usd-us-dollars", amount=1337)

#
# PRO CLIENT
#

pro_client = Client(api_key="YOUR-API-KEY")

# Get historical OHLCV information for a specific coin (USD,BTC)
pro_client.candles("btc-bitcoin", start="2019-01-11T00:00:00Z")

# Get historical ticker information for a specific coin (USD,BTC,ETH)
pro_client.historical("btc-bitcoin", start="2019-04-11T00:00:00Z")

