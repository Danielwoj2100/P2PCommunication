import socket

host = '127.0.0.1'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen(1)
    print('Serwer nasłuchuje na porcie', port)

    client_socket, client_address = server_socket.accept()

    with client_socket:
        print('Nawiązano połączenie z', client_address)

        data = client_socket.recv(1024).decode()
        print('Otrzymane dane od klienta:', data)

        response = 'Odpowiedź od serwera'
        client_socket.send(response.encode())
