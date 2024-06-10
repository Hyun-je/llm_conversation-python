import asyncio
import socket
import json
import time
import uuid


class UDPSender:

    def __init__(self, uuid=str(uuid.uuid4())):
        self.uuid = uuid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_dict(self, message_type, content={}, ip='255.255.255.255', port=8001, verbose=False):
        dict = {
            'uuid': self.uuid, 
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'hostname': socket.gethostname(),
            'message_type': message_type,
            'content': content
        }
        bytes = json.dumps(dict).encode('utf-8')
        self.sock.sendto(bytes, (ip, port))
        if verbose:
            print(f"[{dict['time']}] {dict['uuid'][:8]} -> {message_type} {content}")
        
    async def send_dict_async(self, message_type, content={}, ip='255.255.255.255', port=8001, verbose=False):
        self.send_dict(message_type, content, ip, port, verbose)



if __name__ == '__main__':

    sender = UDPSender()
    count = 0

    while True:

        message_type = 'test'
        content = {
            'message': f'{count} message from {socket.gethostname()}',
        }

        asyncio.run(sender.send_dict_async(message_type, content, verbose=True))

        count += 1
        time.sleep(1)
