import random
import socket
import string

class ErrorGenerator:
    udp_error_rate: float
    broken_connection_rate: float

    def __init__(self, *, udp_error_rate=0, broken_connection_rate=0):
        self.udp_error_rate = udp_error_rate
        self.broken_connection_rate = broken_connection_rate

    # percent - probability of an error in percent range(0-100)
    def break_udp_message(self, message: str) -> str:
        if random.uniform(0, 100) < self.udp_error_rate:
            list_message = list(message)
            broken_index = random.randint(0, len(message))
            current_char = list_message[broken_index]
            characters = string.ascii_letters+string.digits
            new_char = current_char
            while new_char == current_char:
                new_char = random.choice(characters)
            list_message[broken_index] = new_char
            message = ''.join(list_message)
            print(f"Message broken: {message}")
        else:
            print(f"Message correct: {message}")
        return message
    def lost_udp_message(self):
        if random.uniform(0, 100) < self.udp_error_rate:
            print(f"Message not sent")
            return False
        else:
            print(f"Message sent")
            return True


    def break_tcp_session(self, given_socket: socket.socket):
        if random.uniform(0, 100) < self.broken_connection_rate:
            given_socket.close()
