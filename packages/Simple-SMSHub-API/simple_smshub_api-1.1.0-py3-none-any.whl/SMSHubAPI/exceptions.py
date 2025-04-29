class SMSHubAPIException(Exception):
    def __init__(self, message: str = "Default SMSHubAPI Exception"):
        super().__init__(message)


class ApiKeyNotValidException(SMSHubAPIException):
    def __init__(self, message: str = "Invalid API key status"):
        super().__init__(message)


class NoActionException(SMSHubAPIException):
    def __init__(self, message: str = "No action"):
        super().__init__(message)


class BadActionException(SMSHubAPIException):
    def __init__(self, message: str = "General query malformed"):
        super().__init__(message)


class BadServiceException(SMSHubAPIException):
    def __init__(self, message: str = "Incorrect service name"):
        super().__init__(message)


class BadApiKeyException(SMSHubAPIException):
    def __init__(self, message: str = "Invalid API key"):
        super().__init__(message)


class BadCurrencyException(SMSHubAPIException):
    def __init__(self, message: str = "Invalid currency value"):
        super().__init__(message)


class CurrencyChangeUnavailableException(SMSHubAPIException):
    def __init__(self, message: str = "Currency change not available"):
        super().__init__(message)


class SqlErrorException(SMSHubAPIException):
    def __init__(self, message: str = "SQL Server Database Error"):
        super().__init__(message)


class NoBalanceException(SMSHubAPIException):
    def __init__(self, message: str = "The API key has run out of money"):
        super().__init__(message)


class NoNumbersException(SMSHubAPIException):
    def __init__(self, message: str = "There are no numbers with the specified parameters, try again later, or change the operator, country."):
        super().__init__(message)


class WrongServiceException(SMSHubAPIException):
    def __init__(self, message: str = "Invalid service identifier"):
        super().__init__(message)


class NoActivationException(SMSHubAPIException):
    def __init__(self, message: str = "Activation id does not exist"):
        super().__init__(message)


class IncorrectResponseException(SMSHubAPIException):
    def __init__(self, needed: str, got: str):
        super().__init__(f"Invalid responce. Needed \'{needed}\' got \'{got}\'")


class TimeoutException(SMSHubAPIException):
    def __init__(self, message: str = "Timeout while waiting for a sms"):
        super().__init__(message)


class NoCountryException(SMSHubAPIException):
    def __init__(self, message: str = "No country"):
        super().__init__(message)

class ServerException(SMSHubAPIException):
    def __init__(self, message: str = "Server error"):
        super().__init__(message)
