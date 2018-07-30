import socket


class ChatClient:
    def __init__(self, server_name, server_port):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((server_name, server_port))

    def get_name(self):
        return self.__client_socket.getsockname()

    def send_message(self, message):
        self.__client_socket.send(message)

    def receive_message(self):
        try:
            return self.__client_socket.recv(1024)
        except (ConnectionAbortedError, OSError):
            return None

    def close(self):
        self.__client_socket.close()
