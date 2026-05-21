import socket

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 5000

server.bind((host, port))
server.listen(1)

print("SERVER STARTED...")
print("WAITING FOR CLIENT...")

client_socket, address = server.accept()

print(f"CONNECTED TO {address}")

while True:
    # Receive message from client
    message = client_socket.recv(1024).decode()

    if message.lower() == "exit":
        print("Client disconnected")
        break

    print("CLIENT:", message)

    # Send reply
    reply = input("YOU: ")
    client_socket.send(reply.encode())

    if reply.lower() == "exit":
        break

client_socket.close()
server.close()