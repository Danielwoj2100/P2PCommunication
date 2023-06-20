from communiques.enums.CommuniqueType import CommuniqueType
from communiques.enums.StatusCode import StatusCode
from communiques.TransferStatusCommunique import TransferStatusCommunique


class ChecksumFailedCommunique(TransferStatusCommunique):
    def __init__(
        self,
        senders_address=None,
        port=None,
        checksum=None,
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            checksum=checksum,
            status_code=StatusCode.WRONG_CHECKSUM
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        has_fields = len(fields) == 5
        has_right_type = fields[0] == CommuniqueType.TRANSFER_STATUS.value
        has_right_status = fields[2] == StatusCode.WRONG_CHECKSUM.value
        return has_fields and has_right_type and has_right_status
