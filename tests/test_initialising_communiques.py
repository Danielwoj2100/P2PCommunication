from testutils import *


def test_initialise_download_parse():
    received_message = string_initialise_download_test_message()
    communique = InitialiseDownloadCommunique.parse(received_message)
    assert communique.type == CommuniqueType.INITIALISE_DOWNLOAD
    assert communique.senders_address == "1.1.1.1"
    assert communique.port == 0
    assert communique.resource_name == "abc.txt"


def test_initialise_download_full_message():
    communique = initialise_download_test_message()
    assert communique.full_message() == string_initialise_download_test_message()


def test_is_initialise_download():
    assert InitialiseDownloadCommunique.is_message(string_initialise_download_test_message())
    assert InitialiseDownloadCommunique.is_not_message(string_test_confirmation_message())


def test_from_message_initialise_download():
    assert InitialiseDownloadCommunique.from_message(string_initialise_download_test_message())
    assert not InitialiseDownloadCommunique.from_message(string_initialise_transfer_test_message())


def test_initialise_transfer_parse():
    received_message = string_initialise_transfer_test_message()
    communique = InitialiseTransferCommunique.parse(received_message)
    assert communique.type == CommuniqueType.INITIALISE_TRANSFER
    assert communique.senders_address == "1.1.1.1"
    assert communique.port == 0
    assert communique.resource_name == "abc.txt"
    assert communique.total_communique_number == 10


def test_initialise_transfer_full_message():
    communique = initialise_transfer_test_message()
    assert communique.full_message() == string_initialise_transfer_test_message()


def test_is_initialise_transfer():
    assert InitialiseTransferCommunique.is_message(string_initialise_transfer_test_message())
    assert InitialiseTransferCommunique.is_not_message(string_initialise_download_test_message())


def test_from_message_initialise_transfer():
    assert InitialiseTransferCommunique.from_message(string_initialise_transfer_test_message())
    assert not InitialiseTransferCommunique.from_message(string_initialise_download_test_message())
