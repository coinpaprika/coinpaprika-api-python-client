import pytest
import requests_mock

from coinpaprika import client as Coinpaprika
from coinpaprika.exceptions import (
    CoinpaprikaAPIBadRequestException,
    CoinpaprikaAPIException,
    CoinpaprikaAPIForbiddenException,
    CoinpaprikaAPIInternalServerErrorException,
    CoinpaprikaAPINotFoundException,
    CoinpaprikaAPIPaymentRequiredException,
    CoinpaprikaAPITooManyRequestsException,
    CoinpaprikaRequestException,
)

client = Coinpaprika.Client()


def test_invalid_request():
    with pytest.raises(CoinpaprikaRequestException):
        with requests_mock.mock() as m:
            m.get("https://api.coinpaprika.com/v1/coins", text="invalid")
            client.coins()


def test_api_bad_request_exception():
    with pytest.raises(CoinpaprikaAPIBadRequestException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=400,
            )
            client.coin("btc")


def test_api_payment_required_exception():
    with pytest.raises(CoinpaprikaAPIPaymentRequiredException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=402,
            )
            client.coin("btc")


def test_api_api_forbidden_exception():
    with pytest.raises(CoinpaprikaAPIForbiddenException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=403,
            )
            client.coin("btc")


def test_api_not_found_exception():
    with pytest.raises(CoinpaprikaAPINotFoundException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=404,
            )
            client.coin("btc")


def test_api_too_many_requests_exception():
    with pytest.raises(CoinpaprikaAPITooManyRequestsException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc-bitcoin",
                json=json_obj,
                status_code=429,
            )
            client.coin("btc-bitcoin")


def test_api_internal_server_error_exception():
    with pytest.raises(CoinpaprikaAPIInternalServerErrorException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc-bitcoin",
                json=json_obj,
                status_code=500,
            )
            client.coin("btc-bitcoin")


def test_api_exception():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc-bitcoin",
                json=json_obj,
                status_code=400,
            )
            client.coin("btc-bitcoin")


def test_api_exception_invalid_json():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            fake_json_obj = "invalid"
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc-bitcoin",
                json=fake_json_obj,
                status_code=400,
            )
            client.coin("btc-bitcoin")


def test_api_exception_with_no_json():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            m.get("https://api.coinpaprika.com/v1/coins/btc-bitcoin", status_code=400)
            client.coin("btc-bitcoin")


def test_api_global_market():
    expected = {
        "market_cap_usd": 1213374277264,
        "volume_24h_usd": 43738299436,
        "bitcoin_dominance_percentage": 44.53,
    }
    with requests_mock.mock() as m:
        m.get("https://api.coinpaprika.com/v1/global", status_code=200, json=expected)
        result = client.global_market()

    assert result == expected


def test_api_coins():
    expected = [
        {
            "id": "fct-factom",
            "name": "Factom",
            "symbol": "FCT",
            "is_active": False,
            "type": "coin",
        },
        {
            "id": "finale-bens-finale",
            "name": "Bens Finale",
            "symbol": "FINALE",
            "is_active": True,
            "type": "token",
        },
    ]
    with requests_mock.mock() as m:
        m.get("https://api.coinpaprika.com/v1/coins", status_code=200, json=expected)
        result = client.coins()

    assert result == expected


def test_api_coin():
    expected = {
        'id': 'btc-bitcoin',
        'name': 'Bitcoin',
        'symbol': 'BTC',
        "is_active": True,
        "type": "coin",
    }
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin",
            status_code=200,
            json=expected,
        )
        result = client.coin(coin_id="btc-bitcoin")

    assert result == expected


def test_api_twitter():
    expected = {
        'date': '2022-12-12T13:36:47Z',
        'user_name': 'fanquake',
        'is_retweet': True
     }
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/twitter",
            status_code=200,
            json=expected,
        )
        result = client.twitter(coin_id="btc-bitcoin")

    assert result == expected


def test_api_events():
    expected = [
        {"id": "63515-sec-etf-vaneck-decision", "date": "2018-07-10T12:00:00Z"},
        {"id": "62955-super-conference", "date": "2018-09-28T20:00:00Z"},
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/events",
            status_code=200,
            json=expected,
        )
        result = client.events(coin_id="btc-bitcoin")

    assert result == expected


def test_api_exchanges():
    expected = [
        {
            "id": "binance",
            "name": "Binance",
            "fiats": [{"name": "Euro", "symbol": "EUR"}],
        },
        {
            "id": "indoex",
            "name": "Indoex",
            "fiats": [{"name": "US Dollars", "symbol": "USD"}],
        },
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/exchanges",
            status_code=200,
            json=expected,
        )
        result = client.exchanges(coin_id="btc-bitcoin")

    assert result == expected


def test_api_markets():
    expected = [
        {"exchange_id": "binance", "pair": "FIRO/BTC", "category": "Spot"},
        {"exchange_id": "yobit", "pair": "BTC/USDT", "category": "Spot"},
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/markets?category=Spot",
            status_code=200,
            json=expected,
        )
        result = client.markets(coin_id="btc-bitcoin", category="Spot")

    assert result == expected


def test_api_candle():
    expected = [
        {
            "time_open": "2023-05-29T00:00:00Z",
            "time_close": "2023-05-29T23:59:59Z",
            "open": 28105.47629947261,
            "high": 28417.14983419335,
            "low": 27586.800483051946,
            "close": 27760.510213035497,
            "volume": 12695505083,
            "market_cap": 538210000932,
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/latest",
            status_code=200,
            json=expected,
        )
        result = client.candle(coin_id="btc-bitcoin")

    assert result == expected


def test_api_candles():
    expected = [
        {
            "timestamp": "2015-02-18T16:25:00Z",
            "price": 237.74,
            "volume_24h": 26688999,
            "market_cap": 3293041807,
        },
        {
            "timestamp": "2015-02-18T16:30:00Z",
            "price": 237.61,
            "volume_24h": 26784299,
            "market_cap": 3291254941,
        },
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/historical",
            status_code=200,
            json=expected,
        )
        result = client.candles(coin_id="btc-bitcoin")

    assert result == expected


def test_api_today():
    expected = [
        {
            "time_open": "2023-05-30T00:00:00Z",
            "time_close": "2023-05-30T12:41:00Z",
            "open": 27761.43024929449,
            "high": 28035.19508306931,
            "low": 27658.85948325011,
            "close": 27881.16647625301,
            "volume": 11137079269,
            "market_cap": 540564070529,
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/today",
            status_code=200,
            json=expected,
        )
        result = client.today(coin_id="btc-bitcoin")

    assert result == expected


def test_api_people():
    expected = {
        "id": "vitalik-buterin",
        "name": "Vitalik Buterin",
        "description": "Vitalik is the creator of Ethereum ...",
    }
    with requests_mock.mock() as m:
        m.get("https://api.coinpaprika.com/v1/people/1", status_code=200, json=expected)
        result = client.people(person_id=1)

    assert result == expected


def test_api_tags():
    expected = [
        {
            "id": "op-token",
            "name": "Optimism Token",
            "type": "technical",
            "coins": ["usdt-tether", "usdc-usd-coin", "opxvevelo-openx-locked-velo"],
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/tags?additional_fields=coins",
            status_code=200,
            json=expected,
        )
        result = client.tags(additional_fields="coins")

    assert result == expected


def test_api_tag():
    expected = {
        "id": "op-token",
        "name": "Optimism Token",
        "type": "technical",
        "coins": ["usdt-tether", "usdc-usd-coin", "opxvevelo-openx-locked-velo"],
    }
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/tags/op-token?additional_fields=coins",
            status_code=200,
            json=expected,
        )
        result = client.tag(tag_id="op-token", additional_fields="coins")

    assert result == expected


def test_api_tickers():
    expected = [
        {
            "id": "etho-ethoprotocol",
            "name": "Etho Protocol",
            "symbol": "ETHO",
            "quotes": {
                "BTC": {"price": 6.0349609958149e-07, "volume_24h": 10.936540764546796}
            },
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/tickers?quotes=BTC",
            status_code=200,
            json=expected,
        )
        result = client.tickers(quotes="BTC")

    assert result == expected


def test_api_historical():
    expected = [
        {
            "timestamp": "2015-02-18T16:25:00Z",
            "price": 237.74,
            "volume_24h": 26688999,
            "market_cap": 3293041807,
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/tickers/eth-ethereum/historical?quote=BTC",
            status_code=200,
            json=expected,
        )
        result = client.historical(coin_id="eth-ethereum", quote="BTC")

    assert result == expected


def test_api_exchange_list():
    expected = [
        {
            "id": "bitengen",
            "name": "BITENGEN",
            "quotes": {"BTC": {"reported_volume_24h": 0}},
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/exchanges?quotes=BTC",
            status_code=200,
            json=expected,
        )
        result = client.exchange_list(quotes="BTC")

    assert result == expected


def test_api_exchange():
    expected = {
        "id": "bitengen",
        "name": "BITENGEN",
        "quotes": {"BTC": {"reported_volume_24h": 0}},
    }
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/exchanges/bitengen?quotes=BTC",
            status_code=200,
            json=expected,
        )
        result = client.exchange(exchange_id="bitengen", quotes="BTC")

    assert result == expected


def test_api_exchange_markets():
    expected = [
        {
            "pair": "DIA/EUR",
            "quotes": {"USD": {"price": 0.30762038262560004, "volume_24h": 0}},
        }
    ]
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/exchanges/coinbase/markets?quotes=USD",
            status_code=200,
            json=expected,
        )
        result = client.exchange_markets(exchange_id="coinbase", quotes="USD")

    assert result == expected
