from mttkinter import mtTkinter as tK
from functools import partial


class GUI:
    def __init__(self):
        self.window = tK.Tk()
        self.window.title("C. Elegans Connectome Monitor")
        self.window.configure(background='white')

        self.neurons = dict()

        tK.Label(self.window,
                 text="C. ELEGANS CONNECTOME MONITOR",
                 fg='blue',
                 bg='white',
                 font=('Arial', 16, 'bold'))\
            .grid(column=0, row=0, columnspan=30)

        self.time_label = tK.Label(self.window,
                                   text="Simulation time: 4.4s",
                                   fg='orange',
                                   bg='white',
                                   font=('Arial', 12, 'bold'))
        self.time_label.grid(column=0, row=1)

        self.robot_status = tK.Label(self.window,
                                     text="Robot State: DISCONNECTED",
                                     fg='orange',
                                     bg='white',
                                     font=('Arial', 12, 'bold'))
        self.robot_status.grid(column=0, row=2)

    def add_neurons(self, neurons, plotter):
        c = 10
        r = 1
        for k in neurons:
            l = tK.Label(self.window, text=k, fg='black', bg='whitesmoke', font=('Helvetica', 12))
            l.grid(column=c, row=r)
            l.bind("<Button-1>", partial(plotter, key=k))
            self.neurons[k] = l

            if r is 25:
                c += 1
                r = 1
            else:
                r += 1

    def update_neuron(self, key, frequency):
        if frequency > 0:
            self.neurons[key].config(bg='red')
        else:
            self.neurons[key].config(bg='grey90', fg='grey20')
        pass

    def update_time(self, time):
        self.time_label.config(text='Simulation time: {:05.2f}s'.format(time))

    def update_robot_status(self, status):
        if status:
            self.robot_status.config(text='Robot State: CONNECTED')
        else:
            self.robot_status.config(text='Robot State: DISCONNECTED')

    def start(self):
        self.window.mainloop()

    def stop(self):
        self.window.destroy()
