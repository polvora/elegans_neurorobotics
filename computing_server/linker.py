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

        self.last_time = 0
        self.dt = 0
        self.x = 0
        self.enabled = True
        self.robot_speed = 0

        self.left_sensor = [0]*8
        self.right_sensor = [0]*8

    def enable_robot(self, enable):
        self.enabled = enable

    def run(self):
        while self.running:  # Checks if tasks should keep running
            self.server.settimeout(1.0)
            client = None
            if self.enabled:
                try:
                    client, address = self.server.accept()
                except socket.timeout:
                    pass

            if client is not None:
                print("ROBOT LINK: Opening connection")
                self.client_connected = True

                while self.running and self.enabled:  # Checks if tasks should keep running
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
                        # Cuts the new line character out of the string
                        self.receivedMessage = self.receivedMessage[0:-1]
                        # Parses the string and stores the data
                        self.store_sensor_info(self.receivedMessage)
                        # Prints received string to the console
                        print("ROBOT LINK: received: \t\t" + self.receivedMessage)
                        self.receivedMessage = ""  # Prepares string for the next message

                        # Replies the received sensor data with the intended axis positions
                        self.sentMessage = self.compute_axes()
                        client.sendall(self.sentMessage)  # Sends new conformed message to the worm
                        # Prints sent string to the console
                        print("ROBOT LINK: sent: (" + str(self.messageCounter).zfill(5) + ")\t" +
                              self.sentMessage[0:-1])

                print("ROBOT LINK: Closing connection")
                client.close()
                self.client_connected = False

    def stop(self):
        self.running = False
        print('ROBOT LINK: Robotic worm UNLINKED.')

    def is_connected(self):
        return self.client_connected

    def update_time(self, time):
        self.dt = time - self.last_time
        self.last_time = time
        self.x += (self.dt * self.robot_speed)

    def compute_axes(self):
        message = ""
        offset = 10 if self.x < 0 else 0
        for n in range(0, 9):
            axis_angle = 90 + (40 * math.cos(n + (80 * self.x))) + offset
            message += "AX{:d}: {:03.0f} ; ".format(n, axis_angle)

        message += "\n"

        return message

    # From -1 to 1
    def set_speed(self, speed):
        self.robot_speed = speed

    def store_sensor_info(self, message):
        self.left_sensor[0] = int(message[(message.index("SL0: ") + 5): message.index(" ; SL1")])
        self.left_sensor[1] = int(message[(message.index("SL1: ") + 5): message.index(" ; SL2")])
        self.left_sensor[2] = int(message[(message.index("SL2: ") + 5): message.index(" ; SL3")])
        self.left_sensor[3] = int(message[(message.index("SL3: ") + 5): message.index(" ; SL4")])

    def get_left_sensor(self, index):
        return self.left_sensor[index]

    def get_right_sensor(self, index):
        return self.right_sensor[index]
