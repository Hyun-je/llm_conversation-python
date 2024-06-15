import asyncio
import threading
import json
import uuid

class UDPListener:

    def __init__(self, uuid=str(uuid.uuid4()), ip='0.0.0.0', port=8001, callback=None):
        self.ip = ip
        self.port = port
        self.uuid = uuid
        self.callback = callback

    async def listen(self):
        loop = asyncio.get_running_loop()

        # Create datagram endpoint
        transport, _ = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=(self.ip, self.port)
        )

        try:
            while True:
                await asyncio.sleep(1)  # Keep the listener running
        finally:
            transport.close()

    def connection_made(self, transport):
        self.transport = transport
        print(f"Listening on {self.ip}:{self.port}")

    def datagram_received(self, data, addr):
        message = data.decode()
        try:
            json_data = json.loads(message)
            if ('uuid' in json_data) and (json_data['uuid'] != self.uuid):
                if self.callback is not None:
                    self.callback(json_data, addr)
                else:
                    print(f"Received data: {json_data} {addr=}")
        except json.JSONDecodeError:
            print(f"Received non-JSON data: {message}")

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def connection_lost(self, exc):
        print("Connection lost")


if __name__ == '__main__':

    def run():
        listener = UDPListener()
        asyncio.run(listener.listen())

    threading.Thread(target=run).start()

    print("Listener started!")
