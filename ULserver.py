import socket
import threading

# Store connected users
users = {}

def handle_client(client_socket, address):

    # Receive username first
    username = client_socket.recv(1024).decode()

    users[client_socket] = username

    print(f"{username} connected")
    print("Online users:", list(users.values()))

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message.lower() == "exit":
                print(f"{username} disconnected")
                break

            print(f"{username}: {message}")

            # Server response
            reply = f"Hello {username}, message received"
            client_socket.send(reply.encode())

        except:
            break

    # Remove user when disconnected
    del users[client_socket]

    client_socket.close()

    print("Online users:", list(users.values()))
    print("WAITING FOR CLIENTS...")

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 5000

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