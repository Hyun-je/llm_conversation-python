import asyncio
import threading
import time

if __name__ == '__main__':
    from UDP import *
else:
    from . import *



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
            hostname = data['hostname']
            self.device_list[data['uuid']] = {
                'hostname': hostname,
                'address': addr,
                'last_seen': time.time()
            }
            print(f"New device found: {hostname} {addr} {data['uuid']} ")
        else:
            self.device_list[data['uuid']]['last_seen'] = time.time()

    def on_received_unknown(self, data, addr):
        print(f"Warning! Received unknown message: {data} {addr=}")


    async def send_ping(self, interval=2):
        while True:
            await asyncio.sleep(interval)
            message_type = 'device_ping'
            content = {}
            self.sender.send_dict(message_type, content)

    async def remove_inactive_devices(self, interval=3, timeout=6):
        while True:
            await asyncio.sleep(interval)
            current_time = time.time()
            devices_to_remove = []
            for uuid, device in self.device_list.items():
                if current_time - device['last_seen'] > timeout:
                    print(f"Device removed: {device['hostname']} {device['address']} {uuid}")
                    devices_to_remove.append(uuid)
            
            for uuid in devices_to_remove:
                del self.device_list[uuid]

                
    def run_async(self):

        async def send_thread():
            await self.send_ping()

        async def listen_thread():
            await asyncio.gather(
                asyncio.create_task(self.remove_inactive_devices()),
                asyncio.create_task(self.listener.listen())
            )
            
        threading.Thread(target=lambda: asyncio.run(send_thread())).start()
        threading.Thread(target=lambda: asyncio.run(listen_thread())).start()

        
if __name__ == '__main__':
    network_manager = UDPManager()
    network_manager.run_async()

    print("Network manager started!")

    while True:
        print('Device list:')
        time.sleep(2)