import socket
import threading
from datetime import datetime

clients = []
users = {}

# Send to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)


def handle_client(client_socket, address):

    username = client_socket.recv(1024).decode()

    users[client_socket] = username
    clients.append(client_socket)

    print(f"{username} connected")
    print("Online users:", list(users.values()))

    broadcast(f"{username} joined the chat", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message.lower() == "exit":
                print(f"{username} disconnected")
                broadcast(f"{username} left the chat", client_socket)
                break

            # Current time
            current_time = datetime.now().strftime("%I:%M %p")

            # Add timestamp
            full_message = f"[{current_time}] {username}: {message}"

            print(full_message)

            broadcast(full_message, client_socket)

        except:
            break


    # cleanup
    if client_socket in clients:
        clients.remove(client_socket)

    if client_socket in users:
        del users[client_socket]

    client_socket.close()

    print("Online users:", list(users.values()))
    print("WAITING FOR CLIENTS...")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 5001

server.bind((host, port))
server.listen()

print("SERVER STARTED...")
print("WAITING FOR CLIENTS...")

while True:
    client_socket, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    thread.start()

    print("ACTIVE CLIENTS:", threading.active_count()-1)