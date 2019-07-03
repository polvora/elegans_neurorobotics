import socket
from threading import *
import math


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

        self.time = 0

    def run(self):
        while self.running:  # Checks if tasks should keep running
            self.server.settimeout(1.0)
            client = None
            try:
                client, address = self.server.accept()
            except socket.timeout:
                pass

            if client is not None:
                print("ROBOT LINK: Opening connection")
                self.client_connected = True

                while self.running:  # Checks if tasks should keep running
                    client.settimeout(10.0)  # Sets 5 seconds of timeout
                    try:
                        content = client.recv(1)  # Receives the incoming characters one by one
                    except socket.timeout:
                        print("ROBOT LINK: Client dropped")
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
                        print("ROBOT LINK: received: \t\t" + self.receivedMessage)  # Prints received string to the console
                        self.receivedMessage = ""  # Prepares string for the next message

                        # Replies the received sensor data with the intended axis positions
                        self.sentMessage = self.compute_axes()
                        client.sendall(self.sentMessage)  # Sends new conformed message to the worm
                        # Prints sent string to the console
                        print("ROBOT LINK: sent: (" + str(self.messageCounter).zfill(5) + ")\t" + self.sentMessage[0:-1])

                print("ROBOT LINK: Closing connection")
                client.close()
                self.client_connected = False

    def stop(self):
        self.running = False
        print('ROBOT LINK: Robotic worm UNLINKED.')

    def is_connected(self):
        return self.client_connected

    def update_time(self, time):
        self.time = time

    def compute_axes(self):
        message = ""
        for n in range(0, 9):
            axis_angle = 90 + (40*math.cos(n + (10*self.time)))
            message += "AX{:d}: {:03.0f} ; ".format(n, axis_angle)

        message += "\n"
        return message
