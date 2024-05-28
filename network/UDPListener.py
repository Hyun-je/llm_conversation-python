import asyncio
import json

class UDPListener:
    def __init__(self, ip: str, port: int, callback):
        self.ip = ip
        self.port = port
        self.callback = callback

    async def listen(self):
        loop = asyncio.get_running_loop()

        # Create datagram endpoint
        transport, _ = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=(self.ip, self.port))

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
            self.callback(json_data, addr)
        except json.JSONDecodeError:
            print(f"Received non-JSON data: {message}")

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def connection_lost(self, exc):
        print("Connection lost")


if __name__ == '__main__':

    async def main():
        ip = '0.0.0.0'  # Listen on all interfaces
        port = 8001    # Replace with your port

        def callback(data, addr):
            print(f"Received data: {data} {addr=}")

        listener = UDPListener(ip, port, callback)
        await listener.listen()

    # Run the main function
    asyncio.run(main())
