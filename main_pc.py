# import common module
import argparse
import asyncio
import socket
import time
import ollama

# import my module
import network
import voice



async def main(args):

    ip = '0.0.0.0'  # Listen on all interfaces
    port = 8001    # Replace with your port

    print('load voice synth')
    synthesizer = voice.VoiceSynthesizer()


    sender = network.UDPSender()
    answer = input(">>> ")

    dict = {
        'message': answer
    }
    sender.send_dict(dict)

    def callback(data, addr):
        print(f"Received data: {data} {addr=}")

        answer = input(">>> ")

        dict = {
            'message': answer
        }
        sender.send_dict(dict)

        print('synthesis voice...')
        synthesizer.synthesis(dict['message'])

        print('done!')



    
    listener = network.UDPListener(ip, port, sender.uuid, callback)
    print('Ready!')
    await listener.listen()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=False, help='어느 것을 요구하냐')
    parser.add_argument('--env', required=False, default='dev', help='실행환경은 뭐냐')
    args = parser.parse_args()

    asyncio.run(main(args))