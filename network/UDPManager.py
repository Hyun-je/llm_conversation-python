import asyncio
import time
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
        self.device_list = {}
        self.callbacks = {
            'device_ping': self.on_received_device_ping,
            'unknown': self.on_received_unknown
        }

    def add_callback(self, message_type, callback):
        self.callbacks[message_type] = callback

    def on_received_message(self, data, addr):
        message_type = data['message_type']
        if message_type in self.callbacks:
            self.callbacks[message_type](data, addr)
        else:
            self.callbacks['unknown'](data, addr)

    def on_received_device_ping(self, data, addr):
        if data['uuid'] not in self.device_list:
            self.device_list[data['uuid']] = {
                'hostname': data['hostname'],
                'addr': addr,
                'last_seen': time.time()
            }
            print(f"New device found: {data['uuid']} {addr=}")
        else:
            self.device_list[data['uuid']]['last_seen'] = time.time()

    def on_received_unknown(self, data, addr):
        print(f"Warning! Received unknown message: {data} {addr=}")

    def remove_inactive_devices(self, timeout=10):
        current_time = time.time()
        for uuid, device in self.device_list.items():
            if current_time - device['last_seen'] > timeout:
                print(f"Device removed: {uuid}")
                del self.device_list[uuid]

    async def send_ping(self):
        while True:
            await asyncio.sleep(3)
            message_type = 'device_ping'
            content = {}
            self.sender.send_dict(message_type, content)
            self.remove_inactive_devices()

    async def run(self):
        await asyncio.gather(
            asyncio.create_task(self.send_ping()),
            asyncio.create_task(self.listener.listen())
        )
        
        
if __name__ == '__main__':
    
    network_manager = UDPManager()

    asyncio.run(network_manager.run())