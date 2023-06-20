from enum import Enum


class StatusCode(Enum):
    ACCEPT_TRANSFER = 'R0'
    REJECT_TRANSFER = 'R1'
    SUCCESSFUL_TRANSFER = 'TS0'
    END_TRANSFER = 'TS1'
    WRONG_CHECKSUM = 'TS2'

