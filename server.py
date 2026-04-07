import socket
import threading
import ssl
from ping import run_ping
from traceroute import run_traceroute


def process_command(message):
    
    parts = message.split()

    if len(parts) < 2:
        return "Invalid command"

    command = parts[0].upper()
    targets = parts[1:]
    result=""

    if command == "PING":
        for target in targets:
            result+=run_ping(target) + "\n"
    

    elif command == "TRACEROUTE":
        for target in targets:
            result+=run_traceroute(target)+ "\n"

    else:
        return "Unknown command"
    return result

def handle_client(conn,addr):

    print("Connected:", addr)

    try:
        data = conn.recv(1024).decode().strip()

        print("Received:", data)

        result = process_command(data)

        conn.send((result + "\n").encode())

    finally:
        conn.close()

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server listening on port", PORT)

while True:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    conn, addr = server.accept()
    secure_socket = context.wrap_socket(conn, server_side=True)

    thread = threading.Thread(target=handle_client, args=(secure_socket,addr))
    thread.start()