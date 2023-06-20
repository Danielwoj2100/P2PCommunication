import binascii

from communiques.BroadcastCommunique import BroadcastCommunique
from communiques.ChecksumFailedCommunique import ChecksumFailedCommunique
from communiques.ConfirmationCommunique import ConfirmationCommunique
from communiques.InitialiseDownloadCommunique import InitialiseDownloadCommunique
from communiques.InitialiseTransferCommunique import InitialiseTransferCommunique
from communiques.RejectionCommunique import RejectionCommunique
from communiques.SuccessfulTransferCommunique import SuccessfulTransferCommunique
from communiques.TransferCommunique import TransferCommunique
from communiques.enums.CommuniqueType import CommuniqueType
from communiques.enums.StatusCode import StatusCode


def string_test_broadcast_message():
    broadcast_message = f"{CommuniqueType.BROADCAST.value}|255.255.255.255:0|4|A,B,C,D|"
    broadcast_message += f"{binascii.crc32(broadcast_message.encode())}|"
    return broadcast_message


def broadcast_test_message():
    # broadcast_message = f"{CommuniqueType.BROADCAST.value}|255.255.255.255:0|4|A,B,C,D|"
    broadcast_communique = BroadcastCommunique(
        senders_address="255.255.255.255",
        port=0,
        capacity=4,
        resource_names=["A", "B", "C", "D"]
    )
    broadcast_communique.calculate_checksum()
    return broadcast_communique


def string_test_wrong_checksum_message():
    message = f"{CommuniqueType.TRANSFER_STATUS.value}|1.1.1.1:0|{StatusCode.WRONG_CHECKSUM.value}|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def wrong_checksum_test_message():
    communique = ChecksumFailedCommunique(
        senders_address="1.1.1.1",
        port=0
    )
    communique.calculate_checksum()
    return communique


def string_test_successful_message():
    message = f"{CommuniqueType.TRANSFER_STATUS.value}|1.1.1.1:0|{StatusCode.SUCCESSFUL_TRANSFER.value}|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def successful_test_message():
    communique = SuccessfulTransferCommunique(
        senders_address="1.1.1.1",
        port=0
    )
    communique.calculate_checksum()
    return communique


def string_test_confirmation_message():
    message = f"{CommuniqueType.STATUS.value}|1.1.1.1:0|{StatusCode.ACCEPT_TRANSFER.value}|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def confirmation_test_message():
    communique = ConfirmationCommunique(
        senders_address="1.1.1.1",
        port=0
    )
    communique.calculate_checksum()
    return communique


def string_test_rejection_message():
    message = f"{CommuniqueType.STATUS.value}|1.1.1.1:0|{StatusCode.REJECT_TRANSFER.value}|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def rejection_test_message():
    communique = RejectionCommunique(
        senders_address="1.1.1.1",
        port=0
    )
    communique.calculate_checksum()
    return communique


def string_initialise_download_test_message():
    message = f"{CommuniqueType.INITIALISE_DOWNLOAD.value}|1.1.1.1:0|abc.txt|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def initialise_download_test_message():
    communique = InitialiseDownloadCommunique(
        senders_address="1.1.1.1",
        port=0,
        resource_name="abc.txt"
    )
    communique.calculate_checksum()
    return communique


def string_initialise_transfer_test_message():
    message = f"{CommuniqueType.INITIALISE_TRANSFER.value}|1.1.1.1:0|abc.txt|10|"
    message += f"{binascii.crc32(message.encode())}|"
    return message


def initialise_transfer_test_message():
    communique = InitialiseTransferCommunique(
        senders_address="1.1.1.1",
        port=0,
        resource_name="abc.txt",
        total_communique_number=10
    )
    communique.calculate_checksum()
    return communique


def string_transfer_test_message():
    message = f"{CommuniqueType.TRANSFER.value}|1.1.1.1:0|abc.txt|1|2|3|4|"
    message += f"{binascii.crc32(message.encode())}|"
    message += "ABCDEFGH\n"
    return message


def transfer_test_message():
    communique = TransferCommunique(
        senders_address="1.1.1.1",
        port=0,
        resource_name="abc.txt",
        capacity=1,
        start=2,
        end=3,
        communique_index=4,
        data="ABCDEFGH\n".encode()
    )
    communique.calculate_checksum()
    return communique


