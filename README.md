[![Check & test & build](https://github.com/coinpaprika/coinpaprika-api-python-client/actions/workflows/main.yaml/badge.svg)](https://github.com/coinpaprika/coinpaprika-api-python-client/actions/workflows/main.yaml)

# Coinpaprika API Python Client

## Usage

This library provides convenient way to use [Coinpaprika API](https://api.coinpaprika.com/) in Python.

[Coinpaprika](https://coinpaprika.com/) delivers full market data to the world of crypto: coin prices, volumes, market caps, ATHs, return rates and more.

For details and limitations please check the [documentation](https://api.coinpaprika.com/)

## Requirements

```text
pip install coinpaprika
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

## Examples
Check out the [./examples](./examples) directory.

## Tests

```test
pip install -r test_requirements.txt

pytest tests/test_api_request.py
```

## License
CoinpaprikaAPI is available under the MIT license. See the LICENSE file for more info.

## Source
Based on repository which is not maintained anymore: 
[s0h3ck/coinpaprika-api-python-client](https://github.com/s0h3ck/coinpaprika-api-python-client) 
