import socket
import logging
import json


class SocketAPI():
    port: int
    ip: str
    logger: logging.Logger

    def __init__(self, port, ip, logger):
        self.port = port
        self.ip = ip
        self.logger = logger

    def socketServer(self, files_to_transfer):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        self.logger.info(f'Socket server binded to {self.port}')
        s.listen(5)

        filesSent = 0
        while True:
            clientsocket, address = s.accept()
            self.logger.info(f"Connection from {
                             address} has been established!")

            data = "".encode()

            for file in files_to_transfer:
                data += f"{file}\0".encode()
                with open((f'files/{file}'), 'rb') as f:
                    while True:
                        newdata = f.read(1024)
                        if not newdata:
                            break
                        data += newdata
                        filesSent += 1
                data += "\0".encode()

            clientsocket.send(data)
            clientsocket.close()

            if filesSent == len(files_to_transfer):
                s.close()
                break

    def clientSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))

        files = []
        data = s.recv(1024)
        print(data)
        data = data.decode().split("\0")
        for i in range(len(data)):
            if i % 2 == 0:
                files.append(data[i])
            else:
                with open(f'files/{data[i-1]}', 'w') as f:
                    f.write(data[i])

        s.close()

        return files

    def locationServerSocket(self, id, mac, x, y):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        self.logger.info(f'Socket server binded to {self.port}')
        s.listen(5)

        while True:
            clientsocket, address = s.accept()
            self.logger.info(f"Connection from {
                             address} has been established!")

            data = json.dumps(
                {
                    "id": id,
                    "mac": mac,
                    "x": x,
                    "y": y
                }
            ).encode()
            clientsocket.send(data)
            clientsocket.close()
            s.close()
            break

    def locationClientSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))

        data = s.recv(1024)
        data = json.loads(data.decode())

        s.close()

        return data