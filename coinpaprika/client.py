import requests

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


class Client(object):
    _API_FREE_URL = "https://api.coinpaprika.com/v1"
    _API_PRO_URL = "https://api-pro.coinpaprika.com/v1"
    _HEADERS: dict = {"Accept": "application/json", "User-Agent": "coinpaprika/python"}

    def __init__(self, requests_params=None, api_key=None):
        self.session = self._init_session(api_key=api_key)
        self._base_url = self._get_base_url(api_key=api_key)
        self._requests_params = requests_params

    def _init_session(self, api_key=None):
        session = requests.session()
        session.headers.update(
            {**self._HEADERS, "Authorization": api_key} if api_key else self._HEADERS
        )
        return session

    def _get_base_url(self, api_key=None):
        return self._API_PRO_URL if api_key else self._API_FREE_URL

    def _request(self, method, uri, force_params=False, **kwargs):
        kwargs["timeout"] = 10

        data = kwargs.get("data", None)
        if data and isinstance(data, dict):
            kwargs["data"] = data

        # if get request assign data array to params value for requests lib
        if data and (method == "get" or force_params):
            kwargs["params"] = kwargs["data"]
            del kwargs["data"]

        response = getattr(self.session, method)(uri, **kwargs)

        return self._handle_response(response)

    def _create_api_uri(self, path):
        return "{}/{}".format(self._base_url, path)

    def _request_api(self, method, path, **kwargs):
        uri = self._create_api_uri(path)
        return self._request(method, uri, **kwargs)

    def _handle_response(self, response):
        if response.status_code == 400:
            raise CoinpaprikaAPIBadRequestException(response)
        if response.status_code == 402:
            raise CoinpaprikaAPIPaymentRequiredException(response)
        if response.status_code == 403:
            raise CoinpaprikaAPIForbiddenException(response)
        if response.status_code == 404:
            raise CoinpaprikaAPINotFoundException(response)
        if response.status_code == 429:
            raise CoinpaprikaAPITooManyRequestsException(response)
        if response.status_code == 500:
            raise CoinpaprikaAPIInternalServerErrorException(response)
        if not str(response.status_code).startswith("2"):
            raise CoinpaprikaAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise CoinpaprikaRequestException(
                "Invalid Response: {}".format(response.text)
            )

    def _get(self, path, **kwargs):
        return self._request_api("get", path, **kwargs)

    def global_market(self):
        return self._get("global")

    def coins(self):
        return self._get("coins")

    def coin(self, coin_id):
        return self._get("coins/{}".format(coin_id))

    def twitter(self, coin_id):
        return self._get("coins/{}/twitter".format(coin_id))

    def events(self, coin_id):
        return self._get("coins/{}/events".format(coin_id))

    def exchanges(self, coin_id):
        return self._get("coins/{}/exchanges".format(coin_id))

    def markets(self, coin_id, **params):
        return self._get("coins/{}/markets".format(coin_id), data=params)

    def candle(self, coin_id, **params):
        return self._get("coins/{}/ohlcv/latest".format(coin_id), data=params)

    # Deprecated use ohlcv instead
    def candles(self, coin_id, **params):
        return self._get("coins/{}/ohlcv/historical".format(coin_id), data=params)

    def ohlcv(self, coin_id, **params):
        return self._get("coins/{}/ohlcv/historical".format(coin_id), data=params)

    # Deprecated use ohlcv instead
    def today(self, coin_id, **params):
        return self._get("coins/{}/ohlcv/today".format(coin_id), data=params)

    def people(self, person_id):
        return self._get("people/{}".format(person_id))

    def tags(self, **params):
        return self._get("tags", data=params)

    def tag(self, tag_id, **params):
        return self._get("tags/{}".format(tag_id), data=params)

    def tickers(self, **params):
        return self._get("tickers", data=params)

    def ticker(self, coin_id, **params):
        return self._get("tickers/{}".format(coin_id), data=params)

    def historical(self, coin_id, **params):
        return self._get("tickers/{}/historical".format(coin_id), data=params)

    def exchange_list(self, **params):
        return self._get("exchanges", data=params)

    def exchange(self, exchange_id, **params):
        return self._get("exchanges/{}".format(exchange_id), data=params)

    def exchange_markets(self, exchange_id, **params):
        return self._get("exchanges/{}/markets".format(exchange_id), data=params)

    def search(self, **params):
        return self._get("search", data=params)

    def price_converter(self, **params):
        return self._get("price-converter", data=params)
