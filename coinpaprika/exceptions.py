class CoinpaprikaAPIException(Exception):
    def __init__(self, response):
        try:
            json_response = response.json()
        except ValueError:
            self.message = "JSON error message from Coinpaprika: {}".format(
                response.text
            )
        else:
            if "error" not in json_response:
                self.message = "Wrong json format from CoinpaprikaAPI"
            else:
                self.message = json_response["error"]

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):
        return "{}(status_code: {}): {}".format(
            self.__class__.__name__, self.status_code, self.message
        )


class CoinpaprikaAPIBadRequestException(CoinpaprikaAPIException):
    status_code = 400


class CoinpaprikaAPIPaymentRequiredException(CoinpaprikaAPIException):
    status_code = 402


class CoinpaprikaAPIForbiddenException(CoinpaprikaAPIException):
    status_code = 403


class CoinpaprikaAPINotFoundException(CoinpaprikaAPIException):
    status_code = 404


class CoinpaprikaAPITooManyRequestsException(CoinpaprikaAPIException):
    status_code = 429


class CoinpaprikaAPIInternalServerErrorException(CoinpaprikaAPIException):
    status_code = 500


class CoinpaprikaRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "CoinpaprikaRequestException: {}".format(self.message)
