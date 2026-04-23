
import socket
import time   # 👈 ADD THIS

SERVER_IP = "10.245.52.75"   # Change if server is on another laptop
SERVER_PORT = 9999


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("DNS Client Started (type 'exit' to quit)\n")

while True:
    domain = input("Enter domain: ").strip()

    if domain.lower() == "exit":
        break

    if not domain:
        print("Invalid input\n")
        continue

    try:
        start_time = time.time()   # 👈 START TIMER

        client_socket.sendto(domain.encode(), (SERVER_IP, SERVER_PORT))
        response, _ = client_socket.recvfrom(1024)

        end_time = time.time()     # 👈 END TIMER

        print("Resolved IP:", response.decode())
        print("Time taken:", (end_time - start_time), "seconds\n")  # 👈 SHOW TIME

    except Exception as e:
        print("Error:", e)

client_socket.close()