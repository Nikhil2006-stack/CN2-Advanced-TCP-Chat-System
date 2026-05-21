import socket
import threading

client=socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_ip="127.0.0.1"

port=5004

client.connect(
    (server_ip,port)
)


username=input(
    "Enter username: "
)

client.send(
    username.encode()
)


def receive():

    while True:

        try:

            message=client.recv(
                1024
            ).decode()

            print(message)

        except:

            break



receive_thread=threading.Thread(
    target=receive
)

receive_thread.daemon=True

receive_thread.start()



while True:

    message=input()

    if message=="exit":

        client.send(
            message.encode()
        )

        break


    client.send(
        message.encode()
    )


client.close()