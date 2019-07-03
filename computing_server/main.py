from __future__ import print_function
import time
import multiprocessing as mp
import threading
from numba import njit

import matplotlib.pyplot as matlab
from builder import *
from linker import *
from gui import *


def main():
    # file_name = './connectome/c302_A_IClamp.net.nml'
    # file_name = './connectome/c302_A_Syns.net.nml'
    # file_name = './connectome/c302_B_Syns.net.nml'
    file_name = './connectome/c302_B_Full.net.nml'

    linker = Linker("0.0.0.0", 5000)  # Creates link to robotic interface
    gui = GUI()  # Creates new visual monitoring interface

    builder = Builder(file_name) # Builds connectome from NeuroML file
    print("Loaded network file from: " + file_name)
    generators = builder.build_generators()
    print("Found {} generators in network: ".format(len(generators)))
    print(*generators, sep='\n')
    neurons = builder.build_neurons()
    print("Found {} neurons in network: ".format(len(neurons)))
    print(*[v for k, v in neurons.items()], sep='\n')
    synapses = builder.build_synapses()
    print("Found {} synapses in network: ".format(len(synapses)))
    print(*synapses, sep='\n')

    simulation_time = 20
    dt = 0.0002
    T = frange(0, simulation_time, dt)
    V = dict()
    I = dict()
    F = dict()
    # For every neuron  it is created a new time list in V
    [V.setdefault(k, [0] * len(T)) for k in neurons]
    [I.setdefault(k, [0] * len(T)) for k in neurons]
    [F.setdefault(k, [0] * len(T)) for k in neurons]

    start_time = time.time()

    linker.start()  # Starts connection to linked robotic interface
    gui.add_neurons(neurons)  # Adds all the neurons to the table

    def compute():
        update_counter = 0
        for t in range(0, len(T)):
            update_counter += 1

            for generator in generators:
                generator.compute(neurons, T[t])

            for tag in neurons:
                neurons[tag].compute(T[t])

                V[tag][t] = neurons[tag].get_last_voltage()
                I[tag][t] = neurons[tag].get_last_current()
                F[tag][t] = neurons[tag].get_last_frequency()

                if update_counter == 100:
                    gui.update_neuron(tag, F[tag][t])
                elif update_counter > 100:
                    update_counter = 0

            for synapse in synapses:
                synapse.compute(neurons, T[t])

            if T[t]*100 % 1 == 0:
                gui.update_time(T[t])

    threading.Thread(target=compute).start()

    elapsed_time = time.time() - start_time

    print_statistics(simulation_time, dt, elapsed_time, len(generators), len(neurons), len(synapses))
    plot_response(T, V, I, F)


def print_statistics(simulation_time, dt, elapsed_time, n_generators, n_neurons, n_synapses):
    steps = simulation_time / dt
    time_performance = elapsed_time / simulation_time
    steps_performance = steps / elapsed_time
    print('\n' +
          "Network with:\n" +
          "\t{} Generators\n \t{} Neurons\n \t{} Projections\n".format(n_generators, n_neurons, n_synapses) +
          'Simulation parameters:\n' +
          '\tSimulation time: {}[ss]\n'.format(simulation_time) +
          '\tStep time: {}[ss] ({} steps)\n'.format(dt, steps) +
          '\tSteps per simulated second: {}[steps/ss]\n'.format(1 / dt) +
          'Performance stats (real time):\n' +
          '\tElapsed time: {}[rs]\n'.format(elapsed_time) +
          '\tSteps per real second: {}[steps/rs]\n'.format(steps_performance) +
          '\tReal seconds per simulated seconds: {}[rs/ss]'.format(time_performance)
          )


def plot_response(T, V, I, F):
    matlab.subplot(3, 1, 1)
    matlab.plot(T, V['MDR01'])
    matlab.xlabel('Time[s]')
    matlab.ylabel('Voltage[V]')

    matlab.subplot(3, 1, 2)
    matlab.plot(T, I['MDR01'], color='orange')
    matlab.xlabel('Time[s]')
    matlab.ylabel('Current[A]')

    matlab.subplot(3, 1, 3)
    matlab.plot(T, F['MDR01'], color='green')
    matlab.xlabel('Time[s]')
    matlab.ylabel('Frequency[Hz]')

    matlab.show()


if __name__ == '__main__':
    main()
