import communiques.enums.CommuniqueType
from tests.testutils import *


def test_broadcast_communique_parse():
    # message_type, address, capacity, resource_names, checksum = message.split("|")
    received_message = string_test_broadcast_message()
    communique = BroadcastCommunique.parse(received_message)
    assert communique.type == communiques.enums.CommuniqueType.CommuniqueType.BROADCAST
    assert communique.senders_address == "255.255.255.255"
    assert communique.port == 0
    assert communique.capacity == 4
    assert len(communique.resource_names) == 4


def test_broadcast_communique_full_message():
    communique = broadcast_test_message()
    assert communique.full_message() == string_test_broadcast_message()


def test_valid_crc():
    communique = broadcast_test_message()
    assert communique.valid_crc()
    assert not communique.invalid_crc()


def test_invalid_crc():
    communique = broadcast_test_message()
    communique.checksum = communique.checksum + 1
    assert communique.invalid_crc()
    assert not communique.valid_crc()


def test_is_broadcast():
    assert BroadcastCommunique.is_message(string_test_broadcast_message())
    assert BroadcastCommunique.is_not_message("ABCD")


def test_from_message_broadcast():
    assert BroadcastCommunique.from_message(string_test_broadcast_message())
    assert not BroadcastCommunique.from_message("ABCD")



