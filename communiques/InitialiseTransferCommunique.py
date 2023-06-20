from communiques.Communique import Communique
from communiques.enums.CommuniqueType import CommuniqueType


class InitialiseTransferCommunique(Communique):
    resource_name: str
    total_communique_number: int

    def __init__(
            self, *,
            senders_address=None,
            port=None,
            checksum=None,
            resource_name=None,
            total_communique_number=None
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            communique_type=CommuniqueType.INITIALISE_TRANSFER,
            checksum=checksum
        )
        self.resource_name = resource_name
        self.total_communique_number = total_communique_number

    def __str__(self):
        starting_representation = super().__str__()
        addon = "|".join((
            self.resource_name,
            str(self.total_communique_number)
        ))
        return starting_representation + addon + '|'

    @staticmethod
    def parse(message: str):
        message_type, full_address, resource_name, total_communique_number, checksum, _ = message.split("|")
        address, port = full_address.split(":")
        return InitialiseTransferCommunique(
            senders_address=address,
            port=int(port),
            resource_name=resource_name,
            total_communique_number=int(total_communique_number),
            checksum=checksum
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        return len(fields) == 6 and fields[0] == CommuniqueType.INITIALISE_TRANSFER.value
