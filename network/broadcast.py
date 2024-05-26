import asyncio
import socket
import json
import time


class Broadcast:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_dict(self, dict, ip='192.168.0.255', port=8001):
        bytes = json.dumps(dict).encode('utf-8')
        self.sock.sendto(bytes, (ip, port))

    async def send_dict_async(self, dict, ip='192.168.0.255', port=8001):
        self.send_dict(dict, ip, port)



if __name__ == '__main__':

    broadcaster = Broadcast()
    count = 0

    while True:

        dict = {
            'sender': socket.gethostname(),
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count
        }

        asyncio.run(broadcaster.send_dict_async(dict))
        print(f'{socket.gethostname()} -> {dict}')

        count += 1
        time.sleep(1)
