from mttkinter import mtTkinter as tk


class GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("C. Elegans Connectome Monitor")
        self.window.configure(background='white')

        self.neurons = dict()

        tk.Label(self.window,
                 text="C. ELEGANS CONNECTOME MONITOR",
                 fg='blue',
                 bg='white',
                 font=('Arial', 16, 'bold'))\
            .grid(column=0, row=0, columnspan=30)

        self.time_label = tk.Label(self.window,
                                   text="Simulation time: 4.4s",
                                   fg='orange',
                                   bg='white',
                                   font=('Arial', 12, 'bold'))
        self.time_label.grid(column=0, row=1)

    def add_neurons(self, neurons):
        c = 10
        r = 1
        for k in neurons:
            l = tk.Label(self.window, text=k, fg='black', bg='whitesmoke', font=('Helvetica', 12))
            l.grid(column=c, row=r)
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
        print(time)

    def stop(self):
        self.window.destroy()
