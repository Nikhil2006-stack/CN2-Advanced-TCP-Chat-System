import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 5000

server.bind((host, port))

server.listen()

print("SERVER STARTED...")
print("WAITING FOR CLIENT...")

client_socket, address = server.accept()

print(f"CONNECTED TO {address}")

message = client_socket.recv(1024).decode()

print("CLIENT MESSAGE:", message)

client_socket.send("WELCOME CLIENT".encode())

client_socket.close()
server.close()