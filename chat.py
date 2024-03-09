"""e2e chat app using rsa"""

# import modules
import socket
import threading

# external modules
import rsa
from rsa.key import PublicKey

# define variables
server_ip = ""
name = ""
partner_name = ""
ip_gotten = ""
# keys
public_key, private_key = rsa.newkeys(1024)
public_partner = None

# functions

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_gotten = str(s.getsockname()[0])
s.close()

# main code
print("*** chat.py - a simple encrypted chat program ***")
print("")

# ip address finder
try:
    hostname = socket.gethostname()
    ipv4_address = ip_gotten
    print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
except socket.gaierror:
    print("There was an error resolving the hostname.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

name = input("Enter display name:")

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

    print("Waiting for connection...")
    client.send(str(name).encode())
    partner_name = client.recv(1024).decode()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    print("Client Connected!")
elif mode == 2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Please enter the IP address of the hoster: ")
    client.connect((server_ip, 9999))

    partner_name = client.recv(1024).decode()
    client.send(str(name).encode())
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else:
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), pub_key=public_partner))


def receiving_messages(c):
    while True:
        print(f"{partner_name}: " + rsa.decrypt(c.recv(1024), priv_key=private_key).decode())


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
