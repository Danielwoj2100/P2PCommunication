import threading
import time
from socket import SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR, error
from threading import Lock

from communiques.BroadcastCommunique import BroadcastCommunique
from communiques.FinishedTransferCommunique import FinishedTransferCommunique
from communiques.InitialiseDownloadCommunique import InitialiseDownloadCommunique
from communiques.RejectionCommunique import RejectionCommunique
from networkutils import *
from ErrorGenerator import ErrorGenerator


class CommunicationNode:
    def __init__(
            self,
            ip='127.0.0.1',
            port=10001,
            resources=None,
            broadcasting_thread=None,
            receiving_thread=None,
            transferring_threads=None,
            config_file_path=None,
            current_network_status=None,
            error_generator=None,
            asking_thread=None,
            recv_thread=None
    ):
        self.frame_size = 1024
        self.max_header_size = 512
        self.ip = ip
        self.port = port
        self.resources = resources or []
        self.broadcasting_thread = broadcasting_thread
        self.receiving_thread = receiving_thread
        self.transferring_thread = transferring_threads
        self.config_file_path = config_file_path
        self.current_network_status = current_network_status
        self.clients = []
        self.lock = Lock()
        self.nodes_and_files = {}
        self.eg = error_generator or ErrorGenerator()
        self.stop_flag = threading.Event()
        self.asking_thread = asking_thread
        self.stop_recv = threading.Event()
        self.recv_thread = recv_thread

    def __del__(self):
        if self.receiving_thread:
            self.receiving_thread.join()
        if self.transferring_thread:
            self.transferring_thread.join()
        if self.broadcasting_thread:
            self.broadcasting_thread.join()
        if self.recv_thread:
            self.recv_thread.join()

    def update_network_status(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        while var := self.updating():
            self.broadcast_resources(sock)
        print(f"Updating network status: {var}")

    def broadcast_resources(self, local_socket: "socket"):
        broadcast = self.prepare_broadcast_communique()
        original_message = broadcast.full_message()
        # message = self.eg.break_udp_message(original_message)
        if self.eg.lost_udp_message():
            local_socket.sendto(original_message.encode(), ('255.255.255.255', 12345))
        time.sleep(5)

    def prepare_broadcast_communique(self):
        resources_names = self.resources_names()
        return BroadcastCommunique(
            senders_address=self.ip,
            port=self.port,
            capacity=len(resources_names),
            resource_names=resources_names
        )

    def resources_names(self):
        return [
            resource.name
            for resource in self.resources
        ]

    @staticmethod
    def updating():
        return threading.main_thread().is_alive()

    def setup_broadcasting_server(self):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind(('', 12345))
        print(f"{self.ip}:{self.port} Server started. Broadcasting...")
        return server_socket

    def udp_identify(self):
        server_socket = self.setup_broadcasting_server()
        while CommunicationNode.identifying():
            raw_message, address1 = receive_udp_data_chunk(server_socket)
            string_message = raw_message.decode()
            if (broadcast_message := BroadcastCommunique.from_message(string_message)) \
                    and broadcast_message.valid_crc() \
                    and self.not_this_node(broadcast_message.senders_address, broadcast_message.port):
                senders_address = broadcast_message.senders_address
                senders_port = broadcast_message.port
                senders_resources = broadcast_message.resource_names
                with self.lock:
                    self.assign_resources(senders_address, senders_port, senders_resources)
                    if self.unknown_node(senders_address, senders_port):
                        self.clients.append(f"{senders_address}:{senders_port}")
        print(CommunicationNode.identifying())

    def assign_resources(self, senders_address, senders_port, names):
        self.nodes_and_files[f"{senders_address}:{senders_port}"] = names

    def known_node(self, address, port):
        return f"{address}:{port}" in self.clients

    def unknown_node(self, address, port):
        return not self.known_node(address, port)

    def not_this_node(self, senders_address, senders_port):
        return self.ip != senders_address or self.port != senders_port

    def this_node(self, senders_address, senders_port):
        return not self.not_this_node(senders_address, senders_port)

    @staticmethod
    def identifying():
        return threading.main_thread().is_alive()

    def start_broadcasting(self):
        self.broadcasting_thread = threading.Thread(target=self.run_broadcasting_thread)
        self.broadcasting_thread.start()

    def run_broadcasting_thread(self):
        udp_identify = threading.Thread(target=self.udp_identify)
        udp_identify.start()
        update_network_status = threading.Thread(target=self.update_network_status)
        update_network_status.start()
        while var := threading.main_thread().is_alive():
            pass
        print(f"running broadcasting server: {var}")

    def add_resource(self, resource):
        self.resources.append(resource)

    def remove_resource(self, resource_name):
        for i, obj in enumerate(self.resources):
            if obj.name == resource_name:
                del self.resources[i]
                break

    def ask_for_resource_thread(self, resource_name: str, address: str, port: int):
        self.asking_thread = threading.Thread(target=self.ask_for_resource, args=(resource_name, address, port))
        self.asking_thread.start()

    def ask_for_resource(self, resource_name: str, address: str, port: int):
        try:
            with tcp_socket() as client_socket:
                client_socket.connect((address, port))
                print(f"Established connection to {address}:{port}")

                initialise_communique = self.make_download_request(resource_name)
                client_socket.sendall(initialise_communique.full_message().encode())
                print(f"Download initialization for resource {resource_name} sent")

                _, string_response = self.receive_data(client_socket)
                self.handle_download_request_response(string_response, resource_name, client_socket)
        except error as e:
            print("Error sending resource:", str(e))
        finally:
            client_socket.close()
            self.stop_flag.set()  # Ustawienie flagi, aby wątek mógł się zakończyć

    def stop_thread(self):
        if self.asking_thread:
            self.stop_flag.set()  # Ustawienie flagi, aby wątek mógł się zakończyć
            self.asking_thread.join()  # Oczekiwanie na zakończenie wątku

    def handle_download_request_response(self, response: str, resource_name: str, download_socket: "socket"):
        if confirmation := ConfirmationCommunique.from_message(response):
            print(f"Download confirmation for {resource_name} received")
            resource = Resource(name=resource_name)
            self.send_confirmation_communique(download_socket)
            print(f"Confirmation for {resource_name} sent")
            self.download_resource(download_socket, resource)
            download_socket.close()
        elif rejection := RejectionCommunique.from_message(response):
            # Resource transfer was rejected, give the reason
            print("Transfer rejected:", RejectionCommunique.status_code.value)
        else:
            print("Unexpected response:", response)

    def download_resource(self, download_socket: "socket", resource: Resource):
        while CommunicationNode.receiving():
            raw_response, string_response = self.receive_data(download_socket)
            while (transfer_communique := TransferCommunique.from_message(string_response)) \
                    and transfer_communique.invalid_crc():
                self.send_wrong_checksum_transfer(download_socket)
                print("Wrong checksum status sent")
                raw_response, string_response = self.receive_data(download_socket)
            if FinishedTransferCommunique.from_message(string_response):
                print("Received FinishedTransferCommunique")
                self.add_resource(resource)
                break
            elif transfer_communique and transfer_communique.valid_crc():
                print("Received TransferCommunique")
                self.send_successful_transfer(download_socket)
                print("Successful transfer status sent")
                resource.data += transfer_communique.data
                # resource.data[transfer_communique.start, transfer_communique.end] += transfer_communique.data
            else:
                print(f"Undefined response: {string_response}, closing connection")
                break

    def receive_data(self, local_socket: "socket"):
        raw_response = receive_data_chunk(local_socket, self.frame_size + self.max_header_size)
        return raw_response, raw_response.decode()

    def send_successful_transfer(self, local_socket: "socket"):
        created_message = SuccessfulTransferCommunique(senders_address=self.ip, port=self.port)
        local_socket.sendall(created_message.full_message().encode())

    def send_wrong_checksum_transfer(self, local_socket: "socket"):
        created_message = ChecksumFailedCommunique(senders_address=self.ip, port=self.port)
        local_socket.sendall(created_message.full_message().encode())

    def send_confirmation_communique(self, local_socket: "socket"):
        created_message = ConfirmationCommunique(senders_address=self.ip, port=self.port)
        local_socket.sendall(created_message.full_message().encode())

    def send_rejection_communique(self, local_socket: "socket"):
        created_message = RejectionCommunique(senders_address=self.ip, port=self.port)
        local_socket.sendall(created_message.full_message().encode())

    def receive_confirmation_communique(self, client_socket: "socket"):
        response, string_response = self.receive_data(client_socket)
        if not ConfirmationCommunique.from_message(string_response):
            client_socket.close()

    def make_download_request(self, resource_name):
        return InitialiseDownloadCommunique(
            senders_address=self.ip,
            port=self.port,
            resource_name=resource_name
        )

    def listen_for_download(self, connected_client_socket):
        try:
            response, string_response = self.receive_data(connected_client_socket)
            if received_download_request := InitialiseDownloadCommunique.from_message(string_response):
                print(f"Download initialization for resource {received_download_request.resource_name} received")
                self.process_download_request(connected_client_socket, received_download_request)
            else:
                # Invalid message received, close the connection
                print("Invalid message received, closing the connection")
                connected_client_socket.close()
        except error:
            # Handle any socket errors
            print("Error receiving transfer")
        finally:
            connected_client_socket.close()

    def process_download_request(self, client_socket: socket, received_download_request: InitialiseDownloadCommunique):
        if received_download_request.valid_crc():
            requested_resource_name = received_download_request.resource_name
            if found_resource := self.lookup_resource(requested_resource_name):
                # Send ConfirmationCommunique to indicate readiness
                print(f"Sending confirmation for resource {requested_resource_name}")
                self.send_confirmation_communique(client_socket)
                response, string_response = self.receive_data(client_socket)
                if ConfirmationCommunique.from_message(string_response):
                    print(f"Received confirmation for resource {requested_resource_name}")
                    self.send_resource(client_socket, found_resource)
            else:
                # Resource not found
                print(f"Rejecting download for resource {requested_resource_name}")
                self.send_rejection_communique(client_socket)

    def lookup_resource(self, requested_resource_name):
        for local_resource in self.resources:
            if local_resource.name == requested_resource_name:
                return local_resource

    def send_resource(self, client_socket: socket, found_resource: Resource):
        chunks = chunked(found_resource.data, self.frame_size)
        for chunk_index, chunk in enumerate(chunks):
            self.eg.break_tcp_session(client_socket)
            communique = self.prepare_transfer_communique(chunk_index, chunk, found_resource.name)
            encoded_message = communique.full_message().encode()
            # Sending messages and receiving stati until successful
            self.send_until_successful(client_socket, encoded_message)
        self.send_end_communique(client_socket)

    def send_end_communique(self, client_socket):
        end_message = FinishedTransferCommunique(senders_address=self.ip, port=self.port)
        encoded_message = end_message.full_message().encode()
        client_socket.sendall(encoded_message)

    @staticmethod
    def send_until_successful(client_socket: socket, encoded_message):
        client_socket.sendall(encoded_message)
        while (transfer_status := receive_transfer_status(client_socket)) and transfer_status.was_unsuccessful():
            client_socket.sendall(encoded_message)
        print("Transfer message sent and confirmed")

    def prepare_transfer_communique(self, chunk_index: int, chunk, name):
        chunk_length = len(chunk)
        data_start_index = chunk_index * self.frame_size
        data_end_index = data_start_index + chunk_length
        return TransferCommunique(senders_address=self.ip, port=self.port, resource_name=name,
                                  data=chunk, start=data_start_index, end=data_end_index,
                                  capacity=chunk_length,
                                  communique_index=chunk_index
                                  )

    @staticmethod
    def receiving():
        return threading.main_thread().is_alive()

    def listen_for_transfer(self):
        try:
            with tcp_socket() as server_socket:
                server_socket.bind((self.ip, self.port))
                server_socket.listen(5)
                print("Listening for transfers...")
                while self.listening():
                    connected_client_socket, address = server_socket.accept()
                    print(f"Accepted connection from {address}")
                    self.listen_for_download(connected_client_socket)
        except error:
            print("Server socket error while setting up")
        finally:
            server_socket.close()

    @staticmethod
    def listening():
        return True

    def start_communication(self):
        self.recv_thread = threading.Thread(target=self.listen_for_transfer)
        self.recv_thread.start()
