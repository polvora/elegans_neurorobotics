import socket

s = socket.socket()

s.bind(('0.0.0.0', 9000))
s.listen(0)

while True:

    client, address = s.accept()
    print("New client opened a connection")

    while True:
        content = client.recv(32)

        if len(content) == 0:
            break

        else:
            print(content)

    print("Closing connection")
    client.close()
