from communiques.Communique import Communique
from communiques.enums.CommuniqueType import CommuniqueType


class TransferCommunique(Communique):
    resource_name: str
    data: bytearray
    capacity: int
    start: int
    end: int
    communique_index: int

    def __init__(
            self, *,
            senders_address=None,
            port=None,
            checksum=None,
            resource_name=None,
            data=None,
            capacity=None,
            start=None,
            end=None,
            communique_index=None
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            communique_type=CommuniqueType.TRANSFER,
            checksum=checksum
        )
        self.end = end
        self.start = start
        self.capacity = capacity
        self.data = data
        self.resource_name = resource_name
        self.communique_index = communique_index

    def __str__(self):
        starting_representation = super().__str__()
        addon = "|".join((
            self.resource_name,
            str(self.capacity),
            str(self.start),
            str(self.end),
            str(self.communique_index),
        ))
        return starting_representation + addon + '|'

    def full_message(self):
        print(self.data)
        print(type(self.data))
        return super().full_message() + bytearray(self.data).decode('UTF-8')

    @staticmethod
    def parse(message: str):
        message_type, address, resource_name, capacity, start, end, index, checksum, data = message.split("|")
        address_per_se, port = address.split(":")
        return TransferCommunique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum,
            resource_name=resource_name,
            capacity=int(capacity),
            start=int(start),
            end=int(end),
            communique_index=int(index),
            data=bytearray(data.encode())
        )

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        has_fields = len(fields) == 9
        has_right_type = fields[0] == CommuniqueType.TRANSFER.value
        return has_fields and has_right_type

