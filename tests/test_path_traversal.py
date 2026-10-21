"""Regression tests for the id-encoding finding.

Every id-taking method previously formatted the caller's string straight
into the request path. requests/urllib3 remove literal '..' segments before
sending and '#'/'?' cut off the fixed endpoint suffix, so an id such as
'../key/info' could redirect the request to a different endpoint on the
configured host under the operator's key and return that endpoint's
response to the caller.

Each payload below must either raise before any request is made, or result
in the request landing on the method's own fixed endpoint, never on
'/key/info' or '/usage'. No network call is made: requests_mock stubs the
transport.
"""

import pytest
import requests_mock

from coinpaprika import client as Coinpaprika

client = Coinpaprika.Client()

TRAVERSAL_PAYLOADS = [
    "../key/info",
    "../../usage",
    "..%2F..%2Fusage",
    "a/b",
    "x?y=1",
    "x#y",
    "%2e%2e",
    "..\\x",
    "․․",  # U+2024 ONE DOT LEADER
    "．．",  # U+FF0E FULLWIDTH FULL STOP
    "∕",  # U+2215 DIVISION SLASH
    "／",  # U+FF0F FULLWIDTH SOLIDUS
]

# method name -> (callable taking payload, fixed endpoint prefix it must stay under)
SINGLE_ID_METHODS = {
    "coin": (lambda c, p: c.coin(p), "coins"),
    "twitter": (lambda c, p: c.twitter(p), "coins"),
    "events": (lambda c, p: c.events(p), "coins"),
    "exchanges": (lambda c, p: c.exchanges(p), "coins"),
    "markets": (lambda c, p: c.markets(p), "coins"),
    "candle": (lambda c, p: c.candle(p), "coins"),
    "ohlcv": (lambda c, p: c.ohlcv(p), "coins"),
    "today": (lambda c, p: c.today(p), "coins"),
    "people": (lambda c, p: c.people(p), "people"),
    "tag": (lambda c, p: c.tag(p), "tags"),
    "ticker": (lambda c, p: c.ticker(p), "tickers"),
    "historical": (lambda c, p: c.historical(p), "tickers"),
    "exchange": (lambda c, p: c.exchange(p), "exchanges"),
    "exchange_markets": (lambda c, p: c.exchange_markets(p), "exchanges"),
    "contracts": (lambda c, p: c.contracts(p), "contracts"),
}


@pytest.mark.parametrize("method_name", list(SINGLE_ID_METHODS.keys()))
@pytest.mark.parametrize("payload", TRAVERSAL_PAYLOADS)
def test_single_id_methods_never_escape_their_endpoint(method_name, payload):
    call, prefix = SINGLE_ID_METHODS[method_name]
    with requests_mock.mock() as m:
        # Register a catch-all matcher so any request (expected or escaped)
        # gets a response instead of requests_mock raising NoMockAddress,
        # which would hide the real failure mode.
        m.get(requests_mock.ANY, json={})
        try:
            call(client, payload)
        except (ValueError, Exception):
            # Rejecting the id outright is an acceptable, safe outcome.
            # (requests_mock wraps our ValueError in some client error paths,
            # so accept any raised exception here -- the request-url checks
            # below are what actually prove the fix when it doesn't raise.)
            pass
        if not m.request_history:
            return
        for req in m.request_history:
            assert "/key/info" not in req.path
            assert "/usage" not in req.path
            assert req.path.startswith("/v1/{}/".format(prefix))


def test_ticker_by_contract_never_escapes_via_either_id():
    for payload in TRAVERSAL_PAYLOADS:
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, json={})
            try:
                client.ticker_by_contract(payload, "eth-ethereum")
            except Exception:
                pass
            for req in m.request_history:
                assert "/key/info" not in req.path
                assert req.path.startswith("/v1/contracts/")
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, json={})
            try:
                client.ticker_by_contract("eth-ethereum", payload)
            except Exception:
                pass
            for req in m.request_history:
                assert "/key/info" not in req.path
                assert req.path.startswith("/v1/contracts/")


def test_historical_by_contract_never_escapes_via_either_id():
    for payload in TRAVERSAL_PAYLOADS:
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, json={})
            try:
                client.historical_by_contract(payload, "eth-ethereum")
            except Exception:
                pass
            for req in m.request_history:
                assert "/key/info" not in req.path
                assert req.path.startswith("/v1/contracts/")
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, json={})
            try:
                client.historical_by_contract("eth-ethereum", payload)
            except Exception:
                pass
            for req in m.request_history:
                assert "/key/info" not in req.path
                assert req.path.startswith("/v1/contracts/")


def test_exact_audit_payloads_never_reach_key_info():
    cases = [
        ("exchange", ["../key/info"]),
        ("people", ["../key/info"]),
        ("events", ["../key/info#"]),
        ("ticker_by_contract", ["eth-ethereum", "../../key/info"]),
    ]
    for method_name, args in cases:
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, json={})
            try:
                getattr(client, method_name)(*args)
            except Exception:
                pass
            for req in m.request_history:
                assert "/key/info" not in req.path


def test_legitimate_ids_still_work():
    with requests_mock.mock() as m:
        m.get(
            "https://api.coinpaprika.com/v1/exchanges/binance", json={"id": "binance"}
        )
        result = client.exchange("binance")
        assert result == {"id": "binance"}


def test_rejects_empty_dot_and_dotdot_ids():
    for bad in (".", ".."):
        with pytest.raises(ValueError):
            client.exchange(bad)
        with pytest.raises(ValueError):
            client.tag(bad)
