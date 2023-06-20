import socket

host = '127.0.0.1'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))

    message = 'Dane od klienta'
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    print('Odpowiedź od serwera:', response)
