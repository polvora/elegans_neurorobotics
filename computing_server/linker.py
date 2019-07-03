import socket
from threading import *


class Linker(Thread):
    def __init__(self, host, port):
        super(Linker, self).__init__()
        self.server = socket.socket()

        self.host = host
        self.port = port

        self.server.bind((host, port))
        self.server.listen(0)

        self.receivedMessage = ""
        self.sentMessage = ""

        self.messageCounter = 0

        self.running = True

        self.client_connected = False

    def run(self):
        while self.running:  # Checks if tasks should keep running
            self.server.settimeout(1.0)
            client = None
            try:
                client, address = self.server.accept()
            except socket.timeout:
                pass

            if client is not None:
                print("LINKER: Opening connection")
                self.client_connected = True

                while self.running:  # Checks if tasks should keep running
                    client.settimeout(5.0)  # Sets 5 seconds of timeout
                    try:
                        content = client.recv(1)  # Receives the incoming characters one by one
                    except socket.timeout:
                        print("LINKER: Client dropped")
                        client.close()
                        break  # If there is a timeout connection is dropped and server starts listening again
                    # Concatenates the new character to the message
                    self.receivedMessage = self.receivedMessage + content

                    if len(content) == 0:  # If received content is empty, it's the end of the message
                        break

                    if content == '\n':  # End of string
                        self.messageCounter += 1  # Increments the message identifier counter
                        self.receivedMessage = self.receivedMessage[
                                               0:-1]  # Cuts the new line character out of the string
                        print("LINKER: received: \t\t" + self.receivedMessage)  # Prints received string to the console
                        self.receivedMessage = ""  # Prepares string for the next message

                        # Replies the received sensor data with the intended axis positions
                        self.sentMessage = "AX0: 090 ; AX1: 090 ; AX2: 090 ; AX3: 090 ; AX4: 090 ; " + \
                                           "AX5: 090 ; AX6: 090 ; AX7: 090 ; AX8: 090 ; \n"
                        client.sendall(self.sentMessage)  # Sends new conformed message to the worm
                        # Prints sent string to the console
                        print("LINKER: sent: (" + str(self.messageCounter).zfill(5) + ")\t" + self.sentMessage[0:-1])

                print("LINKER: Closing connection")
                client.close()
                self.client_connected = False

    def stop(self):
        self.running = False
        self.server.close()

        print('LINKER: Robotic worm UNLINKED.')

    def is_connected(self):
        return self.client_connected

