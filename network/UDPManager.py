import asyncio
from UDPSender import UDPSender
from UDPListener import UDPListener


class UDPManager:

    def __init__(self):
        self.sender = UDPSender()
        self.listener = UDPListener(
            uuid=self.sender.uuid,
            ip='0.0.0.0',
            port=8001,
            callback=self.on_received_message)
        self.callbacks = {
            'unknown': self.on_received_message_unknown
        }

    def add_callback(self, message_type, callback):
        self.callbacks[message_type] = callback

    def on_received_message(self, data, addr):
        message_type = data['message_type']
        if message_type in self.callbacks:
            self.callbacks[message_type](data, addr)
        else:
            self.callbacks['unknown'](data, addr)

    def on_received_message_unknown(self, data, addr):
        print(f"Warning! Received unknown message: {data} {addr=}")

    async def send_ping(self):
        while True:
            await asyncio.sleep(3)
            message_type = 'device_ping'
            content = {}
            self.sender.send_dict(message_type, content)

    async def run(self):
        await asyncio.gather(
            asyncio.create_task(self.send_ping()),
            asyncio.create_task(self.listener.listen())
        )
        
        
if __name__ == '__main__':
    
    def on_receive_device_ping(data, addr):
        print(f"on_receive_device_ping: {data} {addr=}")

    network_manager = UDPManager()
    network_manager.add_callback('device_ping', on_receive_device_ping)

    asyncio.run(network_manager.run())