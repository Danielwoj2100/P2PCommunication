from socket import socket, AF_INET, SOCK_STREAM

from more_itertools import chunked

from Resource import Resource
from communiques.ChecksumFailedCommunique import ChecksumFailedCommunique
from communiques.SuccessfulTransferCommunique import SuccessfulTransferCommunique
from communiques.TransferCommunique import TransferCommunique
from communiques.enums.CommuniqueType import CommuniqueType
from communiques.ConfirmationCommunique import ConfirmationCommunique
from communiques.enums.StatusCode import StatusCode


def tcp_socket():
    return socket(AF_INET, SOCK_STREAM)


def receive_tcp_data_chunk(local_socket: socket):
    return local_socket.recv(1024)


def receive_udp_data_chunk(local_socket: socket):
    return local_socket.recvfrom(1024)


def send_confirmation_communique(local_socket: socket):
    endpoint, port = local_socket.getpeername()
    created_message = ConfirmationCommunique(senders_address=endpoint, port=port)
    local_socket.sendall(created_message.full_message().encode())


def send_transfer_status(local_socket: socket, status_code: str):
    local_socket.sendall(f'TransferStatusCommunique|{status_code}'.encode())


def successful_transfer(local_socket: socket):
    send_transfer_status(local_socket, StatusCode.SUCCESSFUL_TRANSFER.value.encode())


def wrong_checksum_transfer(local_socket: socket):
    send_transfer_status(local_socket, StatusCode.WRONG_CHECKSUM.value.encode())


def receive_data_chunk(local_socket: socket, size=1024+512):
    return local_socket.recv(size)


def send_data(given_socket: socket, data: bytearray):
    chunks = []
    for i in range(len(data)):
        chunk = data[i:i + 1024]
        chunks.append(chunk)
    for chunk in chunks:
        message = f'TransferCommunique:{chunk}'
        given_socket.sendall(message.encode())


def send_transfer_communique(given_socket: socket, resource: Resource, frame_size=1024):
    chunks = chunked(resource.data, frame_size)
    address, port = given_socket.getsockname()
    for chunk_index, chunk in enumerate(chunks):
        data_start_index = chunk_index * frame_size
        data_end_index = data_start_index + len(chunk)
        communique = TransferCommunique(
            senders_address=address,
            port=port,
            resource_name=resource.name,
            data=chunk,
            start=data_start_index,
            end=data_end_index,
            communique_index=chunk_index
        )
        given_socket.sendall(communique.full_message().encode())


def receive_transfer_status(client_socket):
    response = receive_data_chunk(client_socket)
    string_response = response.decode()
    if success := SuccessfulTransferCommunique.from_message(string_response):
        return success
    elif wrong_checksum := ChecksumFailedCommunique.from_message(string_response):
        return wrong_checksum
    else:
        # Undefined response, terminate connection
        pass


def receive_confirmation_communique(client_socket):
    response = receive_data_chunk(client_socket)
    string_response = response.decode()
    if not ConfirmationCommunique.from_message(string_response):
        client_socket.close()



def receive_transfer(client_socket):
    response = receive_data_chunk(client_socket)
    string_response = response.decode()
    if success := SuccessfulTransferCommunique.from_message(string_response):
        return success
    elif wrong_checksum := ChecksumFailedCommunique.from_message(string_response):
        return wrong_checksum
    else:
        # Undefined response, terminate connection
        pass


def send_end(given_socket: socket):
    given_socket.sendall('END'.encode())


def is_transfer_status_communique(message: str):
    return message.startswith(CommuniqueType.TRANSFER_STATUS.value)


def is_transfer_communique(message: str):
    return message.startswith(CommuniqueType.TRANSFER.value)


def is_confirmation_communique(message: str):
    try:
        # message_type, address, checksum, status
        message_fields = message.split("|")
        has_right_status = message_fields[0] == CommuniqueType.STATUS.value
        has_right_code = message_fields[2] == StatusCode.SUCCESSFUL_TRANSFER
        return has_right_status and has_right_code
    except IndexError:
        return False


def is_rejection_communique(message: str):
    try:
        # message_type, address, checksum, status
        message_fields = message.split("|")
        has_right_status = message_fields[0] == CommuniqueType.STATUS.value
        has_right_code = message_fields[2] == StatusCode.WRONG_CHECKSUM
        return has_right_status and has_right_code
    except IndexError:
        return False


def is_status_communique(message: str):
    try:
        message_fields = message.split("|")
        return message_fields[0] == CommuniqueType.STATUS.value
    except IndexError:
        return False


def is_initialise_download_communique(message: str):
    try:
        message_fields = message.split("|")
        return message_fields[0] == CommuniqueType.INITIALISE_DOWNLOAD.value
    except IndexError:
        return False
