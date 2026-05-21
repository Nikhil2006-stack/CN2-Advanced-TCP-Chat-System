import socket
import threading
from datetime import datetime
import time

clients=[]
users={}
connections={}

def save_log(text):

    with open(
        "chat_history.txt",
        "a"
    ) as file:

        file.write(
            text+"\n"
        )


def broadcast(message,sender=None):

    for client in clients:

        if client!=sender:

            try:

                client.send(
                    message.encode()
                )

            except:
                pass



def handle_client(
        client_socket,
        address
):

    username=client_socket.recv(
        1024
    ).decode()

    users[client_socket]=username

    connections[
        client_socket
    ]=address

    clients.append(
        client_socket
    )

    current_time=(
        datetime.now()
        .strftime(
            "%I:%M %p"
        )
    )

    log=(
        f"{username} connected "
        f"IP:{address[0]} "
        f"Port:{address[1]} "
        f"Time:{current_time}"
    )

    print(log)

    save_log(log)

    broadcast(
        f"{username} joined chat"
    )


    while True:

        try:

            message=(
                client_socket
                .recv(1024)
                .decode()
            )

            if not message:
                break


            if message=="/ping":

                start=time.time()

                client_socket.send(
                    "PONG".encode()
                )

                end=time.time()

                latency=(
                    end-start
                )*1000

                client_socket.send(
                    f"Latency:"
                    f"{latency:.2f} ms"
                    .encode()
                )

                continue


            if message.lower()=="exit":
                break


            now=(
                datetime.now()
                .strftime(
                    "%I:%M %p"
                )
            )

            full_message=(
                f"[{now}] "
                f"{username}: "
                f"{message}"
            )

            print(
                full_message
            )

            save_log(
                full_message
            )

            broadcast(
                full_message,
                client_socket
            )

        except:
            break


    print(
        username,
        "disconnected"
    )

    save_log(
        username+
        " disconnected"
    )


    if client_socket in clients:
        clients.remove(
            client_socket
        )


    if client_socket in users:
        del users[
            client_socket
        ]


    if client_socket in connections:
        del connections[
            client_socket
        ]

    client_socket.close()



def admin_panel():

    while True:

        command=input()

        if command=="/showusers":

            print(
                list(
                    users.values()
                )
            )


        elif command=="/showconnections":

            print(
                "\nConnections"
            )

            for sock,addr in connections.items():

                print(
                    users[sock],
                    "IP:",
                    addr[0],
                    "Port:",
                    addr[1]
                )


        elif command=="/history":

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


        elif command=="/exit":

            print(
                "Server closed"
            )

            for c in clients:
                c.close()

            server.close()

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

server.bind(
    (host,port)
)

server.listen()

print(
    "SERVER STARTED..."
)

print(
    "Protocol: TCP"
)

print(
    "Socket Type:"
    " SOCK_STREAM"
)

print(
    "WAITING..."
)


admin=threading.Thread(
    target=admin_panel
)

admin.daemon=True

admin.start()


while True:

    try:

        client_socket,address=(
            server.accept()
        )

        thread=threading.Thread(
            target=handle_client,
            args=(
                client_socket,
                address
            )
        )

        thread.start()

    except:
        break