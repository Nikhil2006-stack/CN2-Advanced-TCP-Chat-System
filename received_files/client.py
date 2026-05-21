import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"
port = 5000

client.connect((server_ip, port))

client.send("HELLO SERVER".encode())

message = client.recv(1024).decode()

print("SERVER:", message)

client.close()