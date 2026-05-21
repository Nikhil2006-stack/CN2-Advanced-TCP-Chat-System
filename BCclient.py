import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1"
port = 5000

client.connect((server_ip, port))


username = input("Enter username: ")
client.send(username.encode())


# receive messages continuously
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print("\n" + message)
        except:
            print("Disconnected from server")
            client.close()
            break


# send messages
def send_messages():
    while True:
        message = input()

        client.send(message.encode())

        if message.lower() == "exit":
            client.close()
            break


receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()