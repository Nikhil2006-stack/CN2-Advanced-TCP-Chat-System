import socket
import threading
from datetime import datetime

clients = []
users = {}

# Save logs to file
def save_log(text):
    with open("chat_history.txt", "a") as file:
        file.write(text + "\n")


# Send message to all clients
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

    # Receive username
    username = client_socket.recv(1024).decode()

    users[client_socket] = username
    clients.append(client_socket)

    log = f"{username} connected"

    print(log)
    save_log(log)

    print("Online users:", list(users.values()))

    broadcast(f"{username} joined the chat", client_socket)

    while True:

        try:

            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message.lower() == "exit":

                log = f"{username} disconnected"

                print(log)
                save_log(log)

                broadcast(
                    f"{username} left the chat",
                    client_socket
                )

                break

            current_time = datetime.now().strftime("%I:%M %p")

            full_message = (
                f"[{current_time}] "
                f"{username}: {message}"
            )

            print(full_message)

            save_log(full_message)

            broadcast(
                full_message,
                client_socket
            )

        except:
            break

    # Cleanup
    if client_socket in clients:
        clients.remove(client_socket)

    if client_socket in users:
        del users[client_socket]

    client_socket.close()

    print("Online users:", list(users.values()))
    print("WAITING FOR CLIENTS...")


# Server setup
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

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

    print(
        "ACTIVE CLIENTS:",
        threading.active_count()-1
    )