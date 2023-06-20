from communiques.Communique import Communique
from communiques.enums.CommuniqueType import CommuniqueType


class InitialiseDownloadCommunique(Communique):
    resource_name: str

    def __init__(
            self, *,
            senders_address=None,
            port=None,
            checksum=None,
            resource_name=None,
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            communique_type=CommuniqueType.INITIALISE_DOWNLOAD,
            checksum=checksum
        )
        self.resource_name = resource_name

    def __str__(self):
        starting_representation = super().__str__()
        # addon = "|".join((
        #     self.resource_name
        # ))
        return starting_representation + self.resource_name + '|'

    @staticmethod
    def parse(message: str):
        message_type, address, resource_name, checksum, _ = message.split("|")
        address_per_se, port = address.split(":")
        return InitialiseDownloadCommunique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum,
            resource_name=resource_name,
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        return len(fields) == 5 and fields[0] == CommuniqueType.INITIALISE_DOWNLOAD.value


