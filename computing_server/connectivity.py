import socket

s = socket.socket()

s.bind(('0.0.0.0', 9000))
s.listen(0)

receivedMessage = ""
sentMessage = ""

messageCounter = 0

while True:

    client, address = s.accept()
    print("Opening connection")

    while True:
        client.settimeout(5.0)  # Sets 5 seconds of timeout
        try:
            content = client.recv(1)  # Receives the incoming characters one by one
        except socket.timeout:
            print("Client dropped")
            client.close()
            break  # If there is a timeout connection is dropped and server starts listening again
        receivedMessage = receivedMessage + content  # Concatenates the new character to the message

        if len(content) == 0:  # If received content is empty, it's the end of the message
            break

        if content == '\n':  # End of string
            messageCounter += 1  # Increments the message identifier counter
            receivedMessage = receivedMessage[0:-1]  # Cuts the new line character out of the string
            print("received: \t\t" + receivedMessage)  # Prints received string to the console
            receivedMessage = ""  # Prepares string for the next message

            # Replies the received sensor data with the intended axis positions
            sentMessage = "AX0: 090 ; AX1: 090 ; AX2: 090 ; AX3: 090 ; AX4: 090 ; " + \
                          "AX5: 090 ; AX6: 090 ; AX7: 090 ; AX8: 090 ; \n"
            client.sendall(sentMessage)  # Sends new conformed message to the worm
            # Prints sent string to the console
            print("sent: (" + str(messageCounter).zfill(5) + ")\t" + sentMessage[0:-1])

    print("Closing connection")
    client.close()
