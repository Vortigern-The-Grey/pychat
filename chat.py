'''e2e chat app using rsa'''

# import modules
import socket 
import threading

# external modules
import rsa

# define variables
server_ip = ""

# main code
print("*** chat.py - a simple encrypted chat program ***")
print("")

# ip address finder
try:
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
except socket.gaierror:
    print("There was an error resolving the hostname.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
print("")
print("[1] Host a server")
print("[2] Connect to a server")

mode = int(input(">>>"))

# option for hosting chat server
if mode == 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((str(ipv4_address), 9999))
    server.listen()

    client, _ = server.accept()

elif mode == 2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Please enter the IP address of the hoster.")
    client.connect((server_ip, 9999))
else:
    exit()

def sending_messages(c):
    while True:
        message = input(">>> ")
        c.send(message.encode())
        print("You: " + message)

def recieving_messages(c):
    while True:
        print("Partner: " + c.recv(1024).decode())

threading.Thread(target=sending_messages, args=(client,)).start
threading.Thread(target=recieving_messages, args=(client,)).start
