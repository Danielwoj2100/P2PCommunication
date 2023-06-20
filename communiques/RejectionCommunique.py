from communiques.enums.CommuniqueType import CommuniqueType
from communiques.enums.StatusCode import StatusCode
from communiques.StatusCommunique import StatusCommunique


class RejectionCommunique(StatusCommunique):
    def __init__(
            self,
            senders_address=None,
            port=None,
            checksum=None,
    ):
        super().__init__(
            senders_address=senders_address,
            port=int(port),
            communique_type=CommuniqueType.STATUS,
            checksum=checksum,
            status_code=StatusCode.REJECT_TRANSFER
        )

    @staticmethod
    def parse(received_message):
        message_type, address, status_code, checksum, _ = received_message.split("|")
        address_per_se, port = address.split(":")
        return RejectionCommunique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        has_fields = len(fields) == 5
        has_right_type = fields[0] == CommuniqueType.STATUS.value
        has_right_status = fields[2] == StatusCode.REJECT_TRANSFER.value
        return has_fields and has_right_type and has_right_status
