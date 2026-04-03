[![Check & test & build](https://github.com/coinpaprika/coinpaprika-api-python-client/actions/workflows/main.yaml/badge.svg)](https://github.com/coinpaprika/coinpaprika-api-python-client/actions/workflows/main.yaml)

# Coinpaprika API Python Client

## Usage

This library provides convenient way to use [Coinpaprika API](https://api.coinpaprika.com/) in Python.

[Coinpaprika](https://coinpaprika.com/) delivers full market data to the world of crypto: coin prices, volumes, market caps, ATHs, return rates and more.

For details and limitations please check the [documentation](https://api.coinpaprika.com/)

## Requirements

```text
pip install coinpaprika-sdk
```

## Getting started

### Free plan client 
```python
from coinpaprika import client as Coinpaprika

client = Coinpaprika.Client()
```

### Pro plan client
```python
from coinpaprika import client as Coinpaprika

client = Coinpaprika.Client(api_key="YOUR-API-KEY")
```
API KEY can be generated [https://coinpaprika.com/api/](https://coinpaprika.com/api/).

## API Coverage

### Market Data
```python
client.global_market()                    # Global market overview
client.coins()                            # List all coins
client.coin("btc-bitcoin")               # Coin details
client.tickers()                          # All tickers
client.ticker("btc-bitcoin")             # Ticker for specific coin
client.historical("btc-bitcoin", start="2024-01-01")  # Historical tickers (Pro)
```

### OHLCV
```python
client.candle("btc-bitcoin")              # Latest 24h OHLCV
client.ohlcv("btc-bitcoin", start="2024-01-01")  # Historical OHLCV
client.today("btc-bitcoin")              # Today's OHLCV (updates until close)
```

### Exchanges
```python
client.exchange_list()                    # List exchanges
client.exchange("binance")               # Exchange details
client.exchange_markets("binance")       # Markets on exchange
```

### Contracts
```python
client.platforms()                        # List contract platforms
client.contracts("eth-ethereum")          # Contracts on Ethereum
client.ticker_by_contract("eth-ethereum", "0xdac1...")  # Ticker by contract
client.historical_by_contract("eth-ethereum", "0xdac1...", start="2024-01-01")  # Historical by contract
```

### Other
```python
client.search(q="bitcoin")               # Search coins, exchanges, people, tags
client.price_converter(base_currency_id="btc-bitcoin", quote_currency_id="usd-us-dollars", amount=1)
client.coin_mappings()                    # ID mappings to CoinGecko, CMC, etc. (Pro)
client.people("vitalik-buterin")         # Person details
client.tags()                             # List tags
client.tag("blockchain-service")         # Tag details
client.twitter("btc-bitcoin")            # Twitter timeline
client.events("btc-bitcoin")             # Coin events
client.exchanges("btc-bitcoin")          # Exchanges for coin
client.markets("btc-bitcoin")            # Markets for coin
client.key_info()                         # API key usage info (requires key)
client.changelog_ids()                    # Recent changelog IDs (Pro)
```

## Examples
Check out the [./examples](./examples) directory.

## Tests

```bash
pip install -r test_requirements.txt

pytest tests/test_api_request.py
```

## License
See the [LICENSE](./LICENSE) file for more info.

## Source
Based on repository which is not maintained anymore: 
[s0h3ck/coinpaprika-api-python-client](https://github.com/s0h3ck/coinpaprika-api-python-client) 
