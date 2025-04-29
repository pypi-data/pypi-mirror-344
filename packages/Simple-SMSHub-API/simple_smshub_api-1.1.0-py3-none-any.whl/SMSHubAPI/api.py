import time

from mtrequests import PendingPool, get, PendingResponse, PendingRequest

from SMSHubAPI.enums import Currency, Status
from SMSHubAPI.exceptions import *


def exception_for_text(rsp: PendingResponse):
    exception_table = {
        "API_KEY_NOT_VALID": ApiKeyNotValidException,
        "NO_ACTION": NoActionException,
        "BAD_ACTION": BadActionException,
        "BAD_KEY": BadApiKeyException,
        "BAD_SERVICE": BadServiceException,
        "BAD_CURRENCY": BadCurrencyException,
        "ERROR_SQL": SqlErrorException,
        "NO_NUMBERS": NoNumbersException,
        "NO_BALANCE": NoBalanceException,
        "WRONG_SERVICE": WrongServiceException,
        "NO_ACTIVATION": NoActivationException,
        "CURRENCY_CHANGE_UNAVAILABLE": CurrencyChangeUnavailableException,
        "SERVER_ERROR": ServerException
    }

    exception = exception_table.get(rsp.text, None)
    if exception is not None:
        return exception
    return None


class SMSHubAPI:
    API_URL = "https://smshub.org/stubs/handler_api.php"

    def __init__(self, api_key: str, retries: int = 5, delay: int = 1, raise_for_status: bool = False, proxy=None):
        # initial fields
        self.api_key = api_key
        self.retries = retries
        self.delay = delay
        self.raise_for_status = raise_for_status
        self.proxy = proxy
        # generated fields
        self.pending_pool = PendingPool(sessions_count=1, keep_cookies=True)
        # in work fields
        self.activation_id: str | None = None
        self.phone_number: str | None = None

    def _proceed_rsp(self, rsp: PendingResponse) -> PendingResponse | None:
        if not rsp:
            rsp.raise_for_status() if self.raise_for_status else None
            return rsp

        exc = exception_for_text(rsp)
        if exc:
            if self.raise_for_status:
                raise exc()
            return PendingResponse(None, exc(), rsp.pending_request)

        return None

    # API from https://smshub.org/en/info

    def get_numbers_status(
            self,
            country: int = None,
            operator: str = None
    ) -> dict | PendingResponse:
        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "getNumbersStatus",
            "country": country,
            "operator": operator
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        return rsp.json()

    def get_balance(
            self,
            currency: int | Currency = None
    ) -> float | PendingResponse:
        if isinstance(currency, Currency):
            currency = currency.value

        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "getBalance",
            "currency": currency,
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        return float(rsp.text.split(":")[1])

    def get_number(
            self,
            service: str,
            operator: str = None,
            country: int = None,
            max_price: float = None,
            currency: int | Currency = None
    ) -> str | PendingResponse:
        if isinstance(currency, Currency):
            currency = currency.value

        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "getNumber",
            "service": service,
            "operator": operator,
            "country": country,
            "max_price": max_price,
            "currency": currency,
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        self.activation_id, self.phone_number = rsp.text.split(':')[1:]

        return self.phone_number

    def set_status(
            self,
            status: int | Status = None
    ) -> str | PendingResponse:
        if isinstance(status, Status):
            status = status.value

        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "setStatus",
            "id": self.activation_id,
            "status": status
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        return rsp.text

    def get_status(self) -> tuple[str, str | None] | PendingResponse:
        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "getStatus",
            "id": self.activation_id
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        text = rsp.text
        if text.startswith("STATUS_OK") or text.startswith("STATUS_WAIT_RETRY"):
            status, code = text.split(":")
            return status, code
        return text, None

    def get_prices(
            self,
            service: str = None,
            country: int = None,
            currency: int | Currency = None
    ) -> dict | PendingResponse:
        if isinstance(currency, Currency):
            currency = currency.value

        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "getPrices",
            "service": service,
            "country": country,
            "currency": currency
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        return rsp.json()

    def update_api_currency(
            self,
            currency: int | Currency
    ) -> dict | PendingResponse:
        if isinstance(currency, Currency):
            currency = currency.value

        rsp = get(self.API_URL, {
            "api_key": self.api_key,
            "action": "updateApiCurrency",
            "currency": currency
        }, proxies=self.proxy).wrap(self.pending_pool).send(self.retries, self.delay)

        prsp = self._proceed_rsp(rsp)
        if prsp is not None:
            return prsp

        return rsp.json()

    # Wrappers over API

    def sms_sent(self) -> str | PendingResponse:
        """
        [optional]
        :return:
        """
        return self.set_status(Status.sms_sent)

    def sms_retry(self) -> str | PendingResponse:
        return self.set_status(Status.sms_repeat)

    def wait_for_sms(self, interval: int = 1, timeout: int = 60) -> str | PendingResponse:
        start_time = time.time()
        rsp: tuple[str, str | None] | PendingResponse | None = None
        while time.time() - start_time < timeout:
            last_time = time.time()
            rsp = self.get_status()
            if not isinstance(rsp, tuple):
                return rsp
            status, code = rsp
            if status == "STATUS_OK":
                return code
            time.sleep(abs(interval - (time.time() - last_time) * (interval > (time.time() - last_time))))
        else:
            if self.raise_for_status:
                raise TimeoutException()
            return PendingResponse(None, TimeoutException(), rsp.request if isinstance(rsp, PendingResponse) else None)

    def sms_cancel(self) -> str | PendingResponse:
        return self.set_status(Status.cancel_activation)

    def sms_finish(self) -> str | PendingResponse:
        return self.set_status(Status.activation_completed)

    # Other methods

    def clear_activation(self):
        self.activation_id = None
        self.phone_number = None
