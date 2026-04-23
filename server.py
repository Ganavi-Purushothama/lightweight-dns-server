import socket
import threading

# -------------------------------
# LOCAL DNS RECORDS (STATIC)
# -------------------------------
dns_records = {
    "google.com": "142.250.183.206",
    "youtube.com": "142.250.183.238",
    "example.com": "93.184.216.34",
    "github.com": "140.82.114.3"
}

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9999

# -------------------------------
# EXTERNAL DNS RESOLUTION
# -------------------------------
def resolve_external(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "NOT_FOUND"

# -------------------------------
# HANDLE CLIENT REQUEST
# -------------------------------
def handle_request(data, addr, server_socket):
    domain = data.decode().strip()

    print(f"[REQUEST] {domain} from {addr}")

    # Basic input validation (Security requirement)
    if len(domain) == 0 or len(domain) > 100:
        server_socket.sendto(b"INVALID_DOMAIN", addr)
        return

    if not all(c.isalnum() or c in ".-" for c in domain):
        server_socket.sendto(b"INVALID_FORMAT", addr)
        return

    # Check local records
    if domain in dns_records:
        ip = dns_records[domain]
        source = "LOCAL"
    else:
        ip = resolve_external(domain)
        source = "EXTERNAL"

    print(f"[RESOLVED-{source}] {domain} -> {ip}")

    server_socket.sendto(ip.encode(), addr)

# -------------------------------
# START SERVER
# -------------------------------
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print(f"[STARTED] DNS Server running on {SERVER_IP}:{SERVER_PORT}")

    while True:
        data, addr = server_socket.recvfrom(1024)

        # Handle multiple clients using threads
        client_thread = threading.Thread(
            target=handle_request,
            args=(data, addr, server_socket)
        )
        client_thread.start()

if __name__ == "__main__":
    start_server()