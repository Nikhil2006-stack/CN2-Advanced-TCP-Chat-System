import socket
import os

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("127.0.0.1",5002))

while True:

    print("\n1.Send Message")
    print("2.Send File")

    choice=input("Choice: ")

    if choice=="1":

        msg=input("Message: ")

        client.send(msg.encode())

    elif choice=="2":

        filename=input("Enter file name: ")

        if os.path.exists(filename):

            client.send("SEND_FILE".encode())

            client.send(filename.encode())

            filesize=os.path.getsize(filename)

            client.send(str(filesize).encode())

            with open(filename,"rb") as f:

                while True:

                    data=f.read(1024)

                    if not data:
                        break

                    client.send(data)

            print("File sent successfully")

        else:

            print("File not found")