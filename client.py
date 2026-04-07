import socket
import ssl

HOST = "127.0.0.1"
PORT = 5000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname=HOST)

secure_client.connect((HOST, PORT))

command = input("Enter message: ")

secure_client.send((command+"\n").encode())

response = secure_client.recv(1024).decode()
print("Server response:\n", response)

client.close()