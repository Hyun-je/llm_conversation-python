# import common module
import argparse
import asyncio
import time

# import my module
import llm
import voice

from udp_broadcaster import *
from datetime import datetime
import uuid
import threading
import random



class DeviceMonitor:

    def __init__(self):
        self._device_list = {}
        self._lock = threading.Lock()
        self._callbacks = {
            'device_ping': self.on_received_device_ping
        }

    def on_received_device_ping(self, data, addr):
        with self._lock:
            if data['uuid'] not in self._device_list:
                hostname = data['hostname']
                self._device_list[data['uuid']] = {
                    'hostname': hostname,
                    'address': addr,
                    'last_seen': time.time()
                }
                print("\033[32m", f"New device found: {hostname} {addr} {data['uuid']}", "\033[0m", sep="")
            else:
                self._device_list[data['uuid']]['last_seen'] = time.time()


    async def remove_inactive_devices(self, interval=3, timeout=6):
        while True:
            await asyncio.sleep(interval)
            with self._lock:
                current_time = time.time()
                devices_to_remove = []
                for uuid, device in self._device_list.items():
                    if current_time - device['last_seen'] > timeout:
                        print("\033[91m", f"Lost device: {device['hostname']} {device['address']} {uuid}", "\033[0m", sep="")
                        devices_to_remove.append(uuid)
                
                for uuid in devices_to_remove:
                    del self._device_list[uuid]

    def start(self):
        threading.Thread(target=lambda: asyncio.run(self.remove_inactive_devices())).start()


class VoiceMonitor:

    def __init__(self):
        self._is_speaking = False
        self._timeout = 0
        self._callbacks = {
            'start_speaking': self.on_received_start_speaking,
            'end_speaking': self.on_received_end_speaking
        }

    def on_received_start_speaking(self, data, addr):
        self._is_speaking = True
        self._timeout = 600

    def on_received_end_speaking(self, data, addr):
        self._is_speaking = False

    async def timeout_counter(self):
        while True:
            await asyncio.sleep(1)
            if self._timeout > 0:
                self._timeout -= 1
            else:
                self._is_speaking = False

    def start(self):
        threading.Thread(target=lambda: asyncio.run(self.timeout_counter())).start()


class TextGenerationMonitor:

    def __init__(self):
        self._received_text = None
        self._callbacks = {
            'text_generation': self.on_receive_text_generation
        }

    def on_receive_text_generation(self, data, addr):
        # print(f"on_receive_text_generation: {data} {addr=}")
        print(f"Message : {data['content']['message']}")
        print(f"From : {data['uuid']}")
        self._received_text = data['content']['message']




def main(args):

    # Setup voice synthesizer
    print('load voice synth')
    synthesizer = voice.VoiceSynthesizer()

    # Setup llm client
    print('load llm client')
    llm_client = llm.OllamaClient(model='qwen2:0.5b', system_prompt='')

    device_uuid = str(uuid.uuid4())
    print("\033[36m", f"My UUID: {device_uuid}", "\033[0m", sep="")

    listener = UDPListener(uuid=device_uuid)
    listener.start()

    # Run DeviceMonitor
    device_monitor = DeviceMonitor()
    device_monitor.start()
    listener.add_callbacks(device_monitor._callbacks)

    # Run VoiceMonitor
    voice_monitor = VoiceMonitor()
    voice_monitor.start()
    listener.add_callbacks(voice_monitor._callbacks)

    status = 'wait_for_prompt'  # 'wait_for_prompt', 'text_generation', 'wait_for_silent', 'synthesis_voice'
    voice_stream = None

    text_generation_monitor = TextGenerationMonitor()
    listener.add_callbacks(text_generation_monitor._callbacks)

    # Run UDPPeriodicSender for device ping
    def ping_data_callback():
        return 'device_ping', {'device_type': 'talker'}
    ping_sender = UDPPeriodicSender(uuid=device_uuid, interval=1, data_callback=ping_data_callback)
    ping_sender.start()


    sender = UDPSender(uuid=device_uuid)

    if args.mode == 'active':
        time.sleep(5)
        random_device = random.choice(list(device_monitor._device_list.keys()))
        sender.send_dict(
            message_type='text_generation',
            content={
                'receiver': random_device,
                'message': 'hi, what is your name?'
            }
        )


    while True:

        time.sleep(0.5)

        if len(device_monitor._device_list) == 0:
            # Single Mode
            pass

        else:
            
            # Multi Mode
            if status == 'wait_for_prompt':
                if text_generation_monitor._received_text is not None:
                    status = 'text_generation'
                    print("\033[36m", f"{datetime.now()} {status=}", "\033[0m", sep="")

            elif status == 'text_generation':
                received_text = text_generation_monitor._received_text
                text_generation_monitor._received_text = None
                generated_text = llm_client.chat(received_text)[:512]
                filtered_text = ''.join(c for c in generated_text if ord(c) < 128)
                print(f'{generated_text=}')
                print(f'{filtered_text=}')
                voice_stream = synthesizer.make_stream(filtered_text)
                status = 'wait_for_silent'
                random_device = random.choice(list(device_monitor._device_list.keys()))
                sender.send_dict(
                    message_type='text_generation',
                    content={
                        'receiver': random_device,
                        'message': generated_text
                    }
                )
                print("\033[36m", f"{datetime.now()} {status=}", "\033[0m", sep="")

            elif status == 'wait_for_silent':
                if not voice_monitor._is_speaking:
                    status = 'synthesis_voice'
                    print("\033[36m", f"{datetime.now()} {status=}", "\033[0m", sep="")

            elif status == 'synthesis_voice':
                sender.send_dict(
                    message_type='start_speaking',
                    content={}
                )
                synthesizer.play_stram()
                sender.send_dict(
                    message_type='end_speaking',
                    content={}
                )
                status = 'wait_for_prompt'  
                print("\033[36m", f"{datetime.now()} {status=}", "\033[0m", sep="")

            else:
                print("\033[36m", f"Unknown status : {datetime.now()} {status=}", "\033[0m", sep="")
        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', required=True, default='passive')
    args = parser.parse_args()

    main(args)