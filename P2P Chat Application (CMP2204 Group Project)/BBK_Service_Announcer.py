import time
import json
import socket
import threading

print("Welcome to CMP2204 LAN Party! \nWe are going to broadcast your presence to other users every 8 seconds!")
username = input("Please specify your username: ")
broadcast_ip = input("Please enter the IP Address (simply press 'Enter' for localhost): ")
if broadcast_ip == "":
    broadcast_ip = 'localhost'

sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket
sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
ip_address = socket.gethostbyname(socket.gethostname())
broadcast_port = 6000  # The port that other users are listening to

print(f"{username} is broadcasting at ip: {broadcast_ip}, port: {broadcast_port}.")
print("You are currently sharing your username every 8 seconds!")


def send_broadcast():
    while True:
        message = json.dumps({'username': username, 'ip_address': ip_address, 'port': broadcast_port})
        sock_udp.sendto(message.encode(), (broadcast_ip, broadcast_port))  # Broadcasting the message
        time.sleep(8)


if __name__ == "__main__":
    broadcast_thread = threading.Thread(target=send_broadcast)  # Creating a thread to send broadcast messages
    broadcast_thread.start()  # Starting the thread
