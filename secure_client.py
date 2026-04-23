import socket
import ssl

HOST = "10.245.52.75"   # SAME as your DNS server IP
PORT = 8443

context = ssl.create_default_context()

# since self-signed cert
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=HOST)

secure_sock.connect((HOST, PORT))

print("SSL connection established\n")

while True:
    msg = input("Enter command (PING / STATUS / exit): ")

    if msg.lower() == "exit":
        break

    secure_sock.send(msg.encode())
    response = secure_sock.recv(1024).decode()

    print("Server:", response, "\n")

secure_sock.close()