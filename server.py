import socket
from threading import Thread


class ChatServer:
    def __init__(self, server_port):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind(('', server_port))
        self.__server_socket.listen()
        print('Chat server started on port {}.'.format(server_port))
        self.__sockets = [self.__server_socket]
        self.__run()

    def __run(self):
        while True:
            client_socket, address = self.__server_socket.accept()
            self.__sockets.append(client_socket)
            message = 'The client {} has joined the group.'.format(address).encode('ascii')
            self.__broadcast(message)
            t = Thread(target=lambda: self.__receive(client_socket))
            t.start()

    def __receive(self, client_socket):
        while True:
            try:
                received = client_socket.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                break
            if received is not None:
                message = '{}: '.format(client_socket.getpeername()).encode('ascii') + received
                self.__broadcast(message)
            elif client_socket in self.__sockets:
                message = 'The client {} has left the group.'.format(client_socket.getpeername()).encode('ascii')
                self.__broadcast(message)

    def __broadcast(self, message):
        print(message)
        for sock in self.__sockets:
            if sock != self.__server_socket:
                try:
                    sock.send(message)
                except (ConnectionResetError, ConnectionAbortedError):
                    self.__sockets.remove(sock)
                    message = 'The client {} has left the group.'.format(sock.getpeername()).encode('ascii')
                    self.__broadcast(message)


if __name__ == "__main__":
    chat_server = ChatServer(31066)
