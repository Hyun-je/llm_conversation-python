import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8001))

while True:

    msg, addr = sock.recvfrom(1024)
    print(msg)