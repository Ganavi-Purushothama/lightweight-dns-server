import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 8443

def handle_client(conn, addr):
    print(f"[SSL CONNECTED] {addr}")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"[SSL REQUEST] {data}")

            if data == "PING":
                response = "PONG"
            elif data == "STATUS":
                response = "DNS SERVER ACTIVE"
            else:
                response = "INVALID COMMAND"

            conn.send(response.encode())

    except Exception as e:
        print("[SSL ERROR]", e)

    finally:
        conn.close()
        print(f"[SSL DISCONNECTED] {addr}")


def start_ssl_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[SSL SERVER STARTED] on port {PORT}")

    while True:
        client_socket, addr = sock.accept()
        secure_conn = context.wrap_socket(client_socket, server_side=True)

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()


if __name__ == "__main__":
    start_ssl_server()