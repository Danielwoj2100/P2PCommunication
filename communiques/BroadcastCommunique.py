import communiques.Communique
from communiques.enums.CommuniqueType import CommuniqueType


class BroadcastCommunique(communiques.Communique.Communique):
    capacity: int
    resource_names: list[str]

    def __init__(
            self,
            senders_address=None,
            port=None,
            checksum=None,
            capacity=None,
            resource_names=None
    ):
        super().__init__(
            senders_address=senders_address,
            communique_type=CommuniqueType.BROADCAST,
            port=port,
            checksum=checksum,
        )
        self.capacity = capacity
        self.resource_names = resource_names or []

    def __str__(self):
        starting_representation = super().__str__()
        addon = "|".join((
            str(self.capacity),
            ",".join(self.resource_names),
        ))
        return starting_representation + addon + '|'

    @staticmethod
    def parse(message: str):
        message_type, address, _capacity, resource_names, checksum, _ = message.split("|")
        address_per_se, port = address.split(":")
        resource_names = resource_names.split(",")
        return BroadcastCommunique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum,
            capacity=int(_capacity),
            resource_names=resource_names
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        return len(fields) == 6 and fields[0] == CommuniqueType.BROADCAST.value
