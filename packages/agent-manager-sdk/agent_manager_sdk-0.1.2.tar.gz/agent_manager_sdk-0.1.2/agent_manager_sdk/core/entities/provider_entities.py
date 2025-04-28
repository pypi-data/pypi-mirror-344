from enum import Enum


class QuotaUnit(Enum):
    TIMES = 'times'
    TOKENS = 'tokens'
    CREDITS = 'credits'
