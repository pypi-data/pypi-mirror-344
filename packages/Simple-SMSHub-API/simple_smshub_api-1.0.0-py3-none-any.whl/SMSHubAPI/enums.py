from enum import Enum

class Currency(Enum):
    currency_dollar_1 = 643
    currency_dollar_2 = 840


class Status(Enum):
    sms_sent = 1  # optional
    sms_repeat = 3
    activation_completed = 6
    cancel_activation = 8
