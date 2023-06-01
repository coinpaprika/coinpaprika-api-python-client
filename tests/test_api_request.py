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
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=429,
            )
            client.coin("btc")


def test_api_internal_server_error_exception():
    with pytest.raises(CoinpaprikaAPIInternalServerErrorException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=500,
            )
            client.coin("btc")


def test_api_exception():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            json_obj = {"error": "<error message>"}
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=json_obj,
                status_code=400,
            )
            client.coin("btc")


def test_api_exception_invalid_json():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            fake_json_obj = "invalid"
            m.get(
                "https://api.coinpaprika.com/v1/coins/btc",
                json=fake_json_obj,
                status_code=400,
            )
            client.coin("btc")


def test_api_exception_with_no_json():
    with pytest.raises(CoinpaprikaAPIException):
        with requests_mock.mock() as m:
            m.get("https://api.coinpaprika.com/v1/coins/btc", status_code=400)
            client.coin("btc")
