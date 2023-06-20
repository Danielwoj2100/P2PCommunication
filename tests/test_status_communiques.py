# from communiques.enums.CommuniqueType import CommuniqueType
from testutils import *


def test_checksum_failed_parse():
    received_message = string_test_wrong_checksum_message()
    communique = ChecksumFailedCommunique.parse(received_message)
    assert communique.type == CommuniqueType.TRANSFER_STATUS
    assert communique.senders_address == "1.1.1.1"
    assert communique.status_code == StatusCode.WRONG_CHECKSUM


def test_checksum_failed_full_message():
    communique = wrong_checksum_test_message()
    assert communique.full_message() == string_test_wrong_checksum_message()


def test_is_checksum_failed():
    assert ChecksumFailedCommunique.is_message(string_test_wrong_checksum_message())
    assert ChecksumFailedCommunique.is_not_message(string_test_successful_message())


def test_from_message_checksum_failed():
    assert ChecksumFailedCommunique.from_message(string_test_wrong_checksum_message())
    assert not ChecksumFailedCommunique.from_message(string_test_successful_message())


def test_successful_transfer_parse():
    received_message = string_test_successful_message()
    communique = SuccessfulTransferCommunique.parse(received_message)
    assert communique.type == CommuniqueType.TRANSFER_STATUS
    assert communique.senders_address == "1.1.1.1"
    assert communique.status_code == StatusCode.SUCCESSFUL_TRANSFER


def test_successful_transfer_full_message():
    communique = successful_test_message()
    assert communique.full_message() == string_test_successful_message()


def test_is_successful_transfer():
    assert SuccessfulTransferCommunique.is_message(string_test_successful_message())
    assert SuccessfulTransferCommunique.is_not_message(string_test_wrong_checksum_message())


def test_from_message_successful_transfer():
    assert SuccessfulTransferCommunique.from_message(string_test_successful_message())
    assert not SuccessfulTransferCommunique.from_message(string_test_wrong_checksum_message())


def test_confirmation_parse():
    received_message = string_test_confirmation_message()
    communique = ConfirmationCommunique.parse(received_message)
    assert communique.type == CommuniqueType.STATUS
    assert communique.senders_address == "1.1.1.1"
    assert communique.port == 0
    assert communique.status_code == StatusCode.ACCEPT_TRANSFER


def test_confirmation_full_message():
    communique = confirmation_test_message()
    assert communique.full_message() == string_test_confirmation_message()


def test_is_confirmation():
    assert ConfirmationCommunique.is_message(string_test_confirmation_message())
    assert ConfirmationCommunique.is_not_message(string_test_rejection_message())


def test_from_message_confirmation():
    assert ConfirmationCommunique.from_message(string_test_confirmation_message())
    assert not ConfirmationCommunique.from_message(string_test_rejection_message())


def test_rejection_parse():
    received_message = string_test_rejection_message()
    communique = RejectionCommunique.parse(received_message)
    assert communique.type == CommuniqueType.STATUS
    assert communique.senders_address == "1.1.1.1"
    assert communique.port == 0
    assert communique.status_code == StatusCode.REJECT_TRANSFER


def test_rejection_full_message():
    communique = rejection_test_message()
    assert communique.full_message() == string_test_rejection_message()


def test_is_rejection():
    assert RejectionCommunique.is_message(string_test_rejection_message())
    assert RejectionCommunique.is_not_message(string_test_confirmation_message())


def test_from_message_rejection():
    assert RejectionCommunique.from_message(string_test_rejection_message())
    assert not RejectionCommunique.from_message(string_test_confirmation_message())
