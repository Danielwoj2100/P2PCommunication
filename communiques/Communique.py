import binascii

from communiques.enums.CommuniqueType import CommuniqueType


class Communique:
    senders_address: str
    port: int
    type: CommuniqueType
    checksum: int

    def __init__(
            self, *,
            senders_address=None,
            port=None,
            communique_type=None,
            checksum=None
    ):
        self.senders_address = senders_address
        self.port = port
        self.type = communique_type
        self.checksum = checksum

    def __str__(self):
        communique_representation = "|".join((
            self.type.value,
            f"{self.senders_address}:{self.port}",
        ))
        return communique_representation + '|'

    def full_message(self):
        string_representation = str(self)
        self.calculate_checksum()
        return f"{string_representation}{self.checksum}|"

    def valid_crc(self):
        try:
            liczba = int(self.checksum)
            return liczba
        except ValueError:
            liczba = 0
            return liczba
        return liczba == int(binascii.crc32(str(self).encode()))

    def invalid_crc(self):
        return not self.valid_crc()

    def calculate_checksum(self):
        self.checksum = binascii.crc32(str(self).encode())

    @classmethod
    def from_message(cls, message: str):
        if cls.is_message(message):
            return cls.parse(message)

    @staticmethod
    def is_message(message: str):
        fields = message.split("|")
        return len(fields) and fields[0] in CommuniqueType.types()

    @classmethod
    def is_not_message(cls, message: str):
        return not cls.is_message(message)

    @staticmethod
    def parse(message: str):
        message_type, address, checksum, _ = message.split("|")
        address_per_se, port = address.split(":")
        return Communique(
            senders_address=address_per_se,
            port=int(port),
            checksum=checksum,
            communique_type=CommuniqueType(message_type)
        )
