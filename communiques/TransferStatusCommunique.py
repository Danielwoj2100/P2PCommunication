from communiques.enums.CommuniqueType import CommuniqueType
from communiques.enums.StatusCode import StatusCode
from communiques.StatusCommunique import StatusCommunique


class TransferStatusCommunique(StatusCommunique):
    def __init__(
            self,
            senders_address=None,
            port=None,
            checksum=None,
            status_code=None
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            communique_type=CommuniqueType.TRANSFER_STATUS,
            checksum=checksum,
            status_code=status_code
        )

    @staticmethod
    def parse(message: str):
        message_type, address, status_code, checksum, _ = message.split("|")
        address_per_se, port = address.split(":")
        return TransferStatusCommunique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum,
            status_code=StatusCode(status_code)
        )

    def was_successful(self):
        return self.status_code in (StatusCode.SUCCESSFUL_TRANSFER, StatusCode.END_TRANSFER)

    def was_unsuccessful(self):
        return not self.was_successful()

