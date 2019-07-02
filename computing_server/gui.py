from Tkinter import *
from threading import *


class GUI(Thread):
    def __init__(self):
        super(GUI, self).__init__()
        self.window = Tk()
        self.window.title("C. Elegans Connectome Monitor")
        self.window.configure(background='blue')
        #self.window.geometry('300x200')

        self.neurons = dict()

        Label(self.window, text="C. Elegans Connectome Monitor", fg='yellow', bg='blue', font=('Helvetica', 16, 'bold'))\
            .grid(column=0, row=0, columnspan=30)

    def run(self):
        pass
        # self.window.mainloop()

    def add_neurons(self, neurons):
        c = 0
        r = 1
        for k in neurons:
            l = Label(self.window, text=k, fg='yellow', bg='blue', font=('Helvetica', 12, 'bold'))\
                .grid(column=c, row=r)
            self.neurons[k] = l

            if r is 25:
                c += 1
                r = 1
            else:
                r += 1

    def stop(self):
        self.window.destroy()
