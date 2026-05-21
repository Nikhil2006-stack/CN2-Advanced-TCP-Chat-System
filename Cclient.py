import socket

# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"
port = 5000

client.connect((server_ip, port))

while True:
    # Send message
    message = input("YOU: ")
    client.send(message.encode())

    if message.lower() == "exit":
        break

    # Receive reply
    reply = client.recv(1024).decode()

    if reply.lower() == "exit":
        break

    print("SERVER:", reply)

client.close()