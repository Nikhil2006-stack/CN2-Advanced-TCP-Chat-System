import socket
import threading
import os

clients=[]

# Create received_files folder automatically
FOLDER="received_files"

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)


def handle_client(client_socket,address):

    print(address,"connected")

    while True:
        try:
            msg=client_socket.recv(1024).decode()

            if not msg:
                break

            # FILE TRANSFER
            if msg=="SEND_FILE":

                filename=client_socket.recv(1024).decode()

                filesize=int(client_socket.recv(1024).decode())

                filepath=os.path.join(FOLDER,filename)

                with open(filepath,"wb") as f:

                    received=0

                    while received<filesize:

                        data=client_socket.recv(1024)

                        f.write(data)

                        received+=len(data)

                print(filename,"received successfully")

            else:

                print("Message:",msg)

        except:
            break

    client_socket.close()

    print(address,"disconnected")


# SERVER
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="0.0.0.0"
port=5002

server.bind((host,port))

server.listen()

print("SERVER STARTED...")
print("WAITING FOR CLIENTS...")

while True:

    client_socket,address=server.accept()

    thread=threading.Thread(
        target=handle_client,
        args=(client_socket,address)
    )

    thread.start()