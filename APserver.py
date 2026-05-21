import socket
import threading
from datetime import datetime

clients = []
users = {}


def save_log(text):
    with open("chat_history.txt", "a") as file:
        file.write(text + "\n")


def broadcast(message, sender=None):

    for client in clients:

        if client != sender:

            try:
                client.send(message.encode())

            except:
                pass


def handle_client(client_socket, address):

    username = client_socket.recv(1024).decode()

    users[client_socket] = username
    clients.append(client_socket)

    print(f"{username} connected")

    save_log(f"{username} connected")

    while True:

        try:

            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message.lower() == "exit":
                break

            time = datetime.now().strftime("%I:%M %p")

            full_message = (
                f"[{time}] "
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

    print(f"{username} disconnected")

    save_log(
        f"{username} disconnected"
    )

    if client_socket in clients:
        clients.remove(client_socket)

    if client_socket in users:
        del users[client_socket]

    client_socket.close()



def admin_panel():

    while True:

        command = input()

        if command == "/showusers":

            print(
                "\nOnline Users:"
            )

            print(
                list(users.values())
            )


        elif command == "/history":

            try:

                with open(
                    "chat_history.txt",
                    "r"
                ) as file:

                    print(
                        file.read()
                    )

            except:

                print(
                    "No history"
                )


        elif command.startswith("/kick"):

            parts = command.split()

            if len(parts) < 2:
                continue

            target = parts[1]

            for sock,name in list(users.items()):

                if name == target:

                    sock.send(
                        "You were kicked"
                        .encode()
                    )

                    sock.close()

                    print(
                        target,
                        "kicked"
                    )


        elif command == "/exit":

            for c in clients:
                c.close()

            server.close()

            print(
                "Server closed"
            )

            break



server=socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

host="0.0.0.0"
port=5004

server.bind((host,port))

server.listen()

print("SERVER STARTED...")
print("WAITING FOR CLIENTS...")


admin=threading.Thread(
    target=admin_panel
)

admin.daemon=True

admin.start()


while True:

    try:

        client_socket,address=server.accept()

        thread=threading.Thread(
            target=handle_client,
            args=(
                client_socket,
                address
            )
        )

        thread.start()

        print(
            "ACTIVE CLIENTS:",
            threading.active_count()-2
        )

    except:
        break