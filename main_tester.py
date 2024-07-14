from udp_broadcaster import *


def main():

    def ping_data_callback():
        return 'device_ping', {}
    ping_sender = UDPPeriodicSender(interval=1, data_callback=ping_data_callback)
    ping_sender.start()

    sender = UDPSender()

    while True:
        message_type = input('message_type = ')
        content = {}
        if message_type == 'text_generation':
            prompt = input('prompt = ')
            content['message'] = prompt
        
        sender.send_dict(message_type=message_type, content=content)


if __name__ == '__main__':
    main()