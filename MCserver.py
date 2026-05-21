import socket
import threading

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected")

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message.lower() == "exit":
                print(f"{address} disconnected")
                break

            print(f"{address}: {message}")

            # automatic reply
            reply = f"Message received from server"
            client_socket.send(reply.encode())

        except:
            break

    client_socket.close()
    print(f"{address} connection closed")


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