from mttkinter import mtTkinter as tK
from functools import partial


class GUI:
    def __init__(self):
        self.window = tK.Tk()
        self.window.title("C. Elegans Connectome Monitor")
        self.window.configure(background='white')

        self.neurons = dict()

        self.robot_enabling = True

        # Placeholder
        tK.Label(self.window, bg='white').grid(column=50, row=100, padx=10, pady=2)

        tK.Label(self.window,
                 text="C. ELEGANS CONNECTOME MONITOR",
                 fg='cyan3',
                 bg='black',
                 font=('Arial', 16, 'bold'),
                 width=50,
                 height=1)\
            .grid(column=0,
                  row=0,
                  columnspan=30,
                  pady=10)

        tK.Label(self.window,
                 text="Simulation time:",
                 fg='black',
                 bg='white',
                 width=15,
                 anchor=tK.W,
                 font=('Arial', 12))\
            .grid(column=0,
                  row=1,
                  padx=(20, 0))

        self.time_label = tK.Label(self.window,
                                   text="4.4s",
                                   fg='black',
                                   bg='white',
                                   width=15,
                                   anchor=tK.E,
                                   font=('Arial', 12, 'bold'))
        self.time_label.grid(column=1,
                             row=1,
                             padx=(0, 20))

        tK.Label(self.window,
                 text="Robot State:",
                 fg='black',
                 bg='white',
                 width=15,
                 anchor=tK.W,
                 font=('Arial', 12))\
            .grid(column=0,
                  row=2,
                  padx=(20, 0))

        self.robot_status = tK.Label(self.window,
                                     text="DISCONNECTED",
                                     fg='tomato',
                                     bg='white',
                                     width=15,
                                     anchor=tK.E,
                                     font=('Arial', 12, 'bold'))
        self.robot_status.grid(column=1,
                               row=2,
                               padx=(0, 20))

        tK.Label(self.window,
                 text="Robot Control:",
                 fg='black',
                 bg='white',
                 width=15,
                 anchor=tK.W,
                 font=('Arial', 12))\
            .grid(column=0,
                  row=3,
                  padx=(20, 0)
                  )
        self.enable_robot_btn = tK.Button(self.window,
                                          text="Enable",
                                          width=15,
                                          justify=tK.CENTER,
                                          font=('Arial', 8, 'bold italic'),
                                          command=self.enable_robot,
                                          state=tK.DISABLED)
        self.enable_robot_btn.grid(column=1,
                                   row=3)
        self.disable_robot_btn = tK.Button(self.window,
                                           text="Disable",
                                           width=15,
                                           justify=tK.CENTER,
                                           font=('Arial', 8, 'bold italic'),
                                           command=self.disable_robot)
        self.disable_robot_btn.grid(column=1,
                                    row=4)

        # Borders
        tK.Label(self.window,
                 bd=1,
                 relief=tK.SOLID,
                 width=45,
                 height=16,
                 bg='white'
                 ).grid(column=0,
                        row=6,
                        columnspan=2,
                        rowspan=9)

        tK.Label(self.window,
                 text="Mechanosensation:",
                 fg='black',
                 bg='white',
                 width=15,
                 anchor=tK.W,
                 font=('Arial', 12, 'italic')) \
            .grid(column=0,
                  row=6,
                  padx=(20, 0)
                  )

        self.nose_touch_btn = tK.Button(self.window,
                                        text="Nose Touch",
                                        width=15)
        self.nose_touch_btn.grid(column=0,
                                 row=7,
                                 columnspan=2)
        self.neck_touch_btn = tK.Button(self.window,
                                        text="Neck Touch",
                                        width=15)
        self.neck_touch_btn.grid(column=0,
                                 row=9,
                                 columnspan=2)
        self.lside_touch_btn = tK.Button(self.window,
                                         text="L. Side Touch",
                                         width=15)
        self.lside_touch_btn.grid(column=0,
                                  row=11)
        self.rside_touch_btn = tK.Button(self.window,
                                         text="R. Side Touch",
                                         width=15)
        self.rside_touch_btn.grid(column=1,
                                  row=11)
        self.tail_touch_btn = tK.Button(self.window,
                                        text="Tail Touch",
                                        width=15)
        self.tail_touch_btn.grid(column=0,
                                 row=13,
                                 columnspan=2)


    def disable_robot(self):
        self.enable_robot_btn.config(state=tK.NORMAL)
        self.disable_robot_btn.config(state=tK.DISABLED)
        self.robot_enabling = False

    def enable_robot(self):
        self.enable_robot_btn.config(state=tK.DISABLED)
        self.disable_robot_btn.config(state=tK.NORMAL)
        self.robot_enabling = True

    def is_robot_enabled(self):
        return self.robot_enabling

    def add_neurons(self, neurons, plotter):
        c = 10
        r = 1
        for k in neurons:
            l = tK.Label(self.window,
                         text=k,
                         fg='black',
                         bg='whitesmoke',
                         bd=1,
                         relief=tK.SOLID,
                         width=8,
                         font=('Helvetica', 12)
                         )
            l.grid(column=c,
                   row=r,
                   padx=1,
                   pady=2,
                   )
            l.bind("<Button-1>", partial(plotter, key=k))
            self.neurons[k] = l

            if r is 25:
                c += 1
                r = 1
            else:
                r += 1

    def update_neuron(self, key, frequency):
        if frequency > 0:
            self.neurons[key].config(bg='tomato')
        else:
            self.neurons[key].config(bg='whitesmoke',
                                     fg='grey20')

    def update_time(self, time):
        self.time_label.config(text='{:05.2f}s'.format(time))

    def update_robot_status(self, status):
        if self.robot_enabling:
            if status:
                self.robot_status.config(text='CONNECTED',
                                         fg='chartreuse3')
            else:
                self.robot_status.config(text='DISCONNECTED',
                                         fg='tomato')
        else:
            self.robot_status.config(text='DISABLED',
                                     fg='gold2')

    def start(self):
        self.window.mainloop()

    def stop(self):
        self.window.destroy()
