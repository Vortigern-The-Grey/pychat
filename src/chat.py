"""e2e chat app using rsa"""

# import modules
import socket
import threading

# external modules
import rsa

# define variables
server_ip = ""
name = ""
partner_name = ""
ip_local = ""
ip_mode = 0

# keys
public_key, private_key = rsa.newkeys(1024)
public_partner = None

# main code
print("*** chat.py - a simple encrypted chat program ***")
print("")

# ip address finder
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = str(s.getsockname()[0])
    s.close()
    hostname = socket.gethostname()
    print(f"Internal IPv4 Address for {hostname}: {ip_local}")
except socket.gaierror:
    print("There was an error resolving the hostname.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

name = input("Enter display name:")
ipv4_address = ip_local
print("")
print("[1] Host a server")
print("[2] Connect to a server")

mode = int(input(">>>"))

# option for hosting chat server
if mode == 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((str(ipv4_address), 9999))
    server.listen()

    print("Waiting for connection...")
    client, _ = server.accept()

    client.send(str(name).encode())
    partner_name = client.recv(1024).decode()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    print(f"{partner_name} just connected!")
elif mode == 2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Please enter the IP address of the hoster: ")

    print(f"Connecting to {server_ip}...")

    client.connect((server_ip, 9999))
    partner_name = client.recv(1024).decode()
    client.send(str(name).encode())
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    print(f"Sucessfully connected to {partner_name}")
else:
    exit()


def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), pub_key=public_partner))
        if message.lower() == "/quit":
            print("Chat program terminated.")
            break


def receiving_messages(c):
    while True:
        received_message = rsa.decrypt(c.recv(1024), priv_key=private_key).decode()
        print(f"{partner_name}: {received_message}")
        if received_message.lower() == "/quit":
            print(f"Chat program terminated by {partner_name}.")
            break


sending_thread = threading.Thread(target=sending_messages, args=(client,))
receiving_thread = threading.Thread(target=receiving_messages, args=(client,))

sending_thread.start()
receiving_thread.start()

# close threads
sending_thread.join()
receiving_thread.join()
print("All threads terminated. Chat program closed.")
quit()
