import socket
import json
import time


class Receive:

    def __init__(self, ip='', port=8001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

    def receive_dict(self):
        bytes, addr = self.sock.recvfrom(1024)
        dict = json.loads(bytes.decode('utf-8'))
        return dict

    async def receive_dict_async(self, dict):
        return self.receive_dict()


if __name__ == '__main__':

    receiver = Receive()

    while True:

        dict = receiver.receive_dict()
        print(f'{socket.gethostname()} <- {dict}')
