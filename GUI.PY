import socket
import time
import ssl
import tkinter as tk
from tkinter import messagebox

# --------------------------
# CONFIG
# --------------------------
SERVER_IP = "10.245.52.75"
DNS_PORT = 9999
SSL_PORT = 8443

# --------------------------
# DNS FUNCTION
# --------------------------
def resolve_domain():
    domain = entry_domain.get().strip()

    if not domain:
        messagebox.showerror("Error", "Enter a domain")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        start = time.time()
        client_socket.sendto(domain.encode(), (SERVER_IP, DNS_PORT))
        response, _ = client_socket.recvfrom(1024)
        end = time.time()

        result_ip.config(text=f"IP: {response.decode()}")
        result_time.config(text=f"Time: {round(end-start, 4)} sec")

        client_socket.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------------------
# SSL FUNCTION
# --------------------------
def send_ssl_command(command):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=SERVER_IP)

        secure_sock.connect((SERVER_IP, SSL_PORT))

        secure_sock.send(command.encode())
        response = secure_sock.recv(1024).decode()

        ssl_result.config(text=f"Response: {response}")

        secure_sock.close()

    except Exception as e:
        messagebox.showerror("SSL Error", str(e))


# --------------------------
# GUI WINDOW
# --------------------------
root = tk.Tk()
root.title("Lightweight DNS System")
root.geometry("400x400")
root.config(bg="#1e1e2f")

# --------------------------
# TITLE
# --------------------------
title = tk.Label(root, text="DNS Resolver GUI", font=("Arial", 16, "bold"), bg="#1e1e2f", fg="white")
title.pack(pady=10)

# --------------------------
# DNS SECTION
# --------------------------
tk.Label(root, text="Enter Domain:", bg="#1e1e2f", fg="white").pack()

entry_domain = tk.Entry(root, width=30)
entry_domain.pack(pady=5)

tk.Button(root, text="Resolve", command=resolve_domain, bg="#4CAF50", fg="white").pack(pady=5)

result_ip = tk.Label(root, text="IP: ", bg="#1e1e2f", fg="cyan")
result_ip.pack()

result_time = tk.Label(root, text="Time: ", bg="#1e1e2f", fg="cyan")
result_time.pack()

# --------------------------
# SSL SECTION
# --------------------------
tk.Label(root, text="\nSecure Control", font=("Arial", 12, "bold"), bg="#1e1e2f", fg="white").pack()

tk.Button(root, text="PING", command=lambda: send_ssl_command("PING"), bg="#2196F3", fg="white").pack(pady=3)

tk.Button(root, text="STATUS", command=lambda: send_ssl_command("STATUS"), bg="#FF9800", fg="white").pack(pady=3)

ssl_result = tk.Label(root, text="Response: ", bg="#1e1e2f", fg="yellow")
ssl_result.pack(pady=10)

# --------------------------
# RUN
# --------------------------
root.mainloop()