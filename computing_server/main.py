import socket

s = socket.socket()

s.bind(('0.0.0.0', 9000))
s.listen(0)

message = ""

while True:

    client, address = s.accept()
    print("Opening connection")

    while True:
        client.settimeout(5.0)
        try:
            content = client.recv(1)
        except socket.timeout:
            print("Client dropped")
            break
        message = message + content

        if len(content) == 0:
            break

        if content == '\n':
            print(message[0:-1])
            message = ""

    print("Closing connection")
    client.close()
