from testutils import *


def test_transfer_parse():
    received_message = string_transfer_test_message()
    communique = TransferCommunique.parse(received_message)
    assert communique.type == CommuniqueType.TRANSFER
    assert communique.senders_address == "1.1.1.1"
    assert communique.port == 0
    assert communique.resource_name == "abc.txt"
    assert communique.capacity == 1
    assert communique.start == 2
    assert communique.end == 3
    assert communique.communique_index == 4
    assert communique.data.decode() == "ABCDEFGH\n"


def test_transfer_full_message():
    communique = transfer_test_message()
    assert communique.full_message() == string_transfer_test_message()


def test_is_transfer():
    assert TransferCommunique.is_message(string_transfer_test_message())
    assert TransferCommunique.is_not_message(string_test_successful_message())


def test_from_message_transfer():
    assert TransferCommunique.from_message(string_transfer_test_message())
    assert not TransferCommunique.from_message(string_test_successful_message())
