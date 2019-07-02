from Tkinter import *
from threading import *


class GUI(Thread):
    def __init__(self):
        super(GUI, self).__init__()

        self.window = Tk()
        self.window.title("TERST 001")
        self.window.geometry('300x200')

    def run(self):
        self.window.mainloop()

    def stop(self):
        self.window.destroy()
