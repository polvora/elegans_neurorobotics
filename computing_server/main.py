from __future__ import print_function
import time
# import multiprocessing as mp
import threading
# from numba import njit
import time

import matplotlib.pyplot as matlab
from builder import *
from linker import *
from gui import *

max_simulation_time = 100
dt = 0.002
T = frange(0, max_simulation_time, dt)
V = dict()
I = dict()
F = dict()

current_time = 0
running = True


def main():
    global T, V, I, F, running

    # file_name = './connectome/c302_A_IClamp.net.nml'
    # file_name = './connectome/c302_A_Syns.net.nml'
    # file_name = './connectome/c302_B_Syns.net.nml'
    file_name = './connectome/c302_B_Full.net.nml'
    # file_name = './connectome/c302_A_Full.net.nml'

    linker = Linker("0.0.0.0", 5000)  # Creates link to robotic interface
    gui = GUI()  # Creates new visual monitoring interface

    builder = Builder(file_name)  # Builds connectome from NeuroML file
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

    # For every neuron  it is created a new time list in V
    [V.setdefault(k, [0] * len(T)) for k in neurons]
    [I.setdefault(k, [0] * len(T)) for k in neurons]
    [F.setdefault(k, [0] * len(T)) for k in neurons]

    start_time = time.time()

    linker.start()  # Starts connection to linked robotic interface
    gui.add_neurons(neurons, plot_response)  # Adds all the neurons to the table

    def compute():
        global current_time, running
        update_counter = 0
        t = 0
        fw = list()
        bw = list()
        lw = list()
        rw = list()
        for t in range(0, len(T)):
            for generator in generators:
                generator.compute(neurons, T[t])

            for tag in neurons:
                neurons[tag].compute(T[t])

                V[tag][t] = neurons[tag].get_last_voltage()
                I[tag][t] = neurons[tag].get_last_current()
                F[tag][t] = neurons[tag].get_last_frequency()

                # Updates the GUI each 100 ticks
                if update_counter == 10:
                    gui.update_neuron(tag, F[tag][t])
                elif update_counter > 10:
                    update_counter = 0

            if update_counter == 1:
                print('PVC: ' + str(F['PVCL'][t] + F['PVCR'][t]))
                print('AVB: ' + str(F['AVBL'][t] + F['AVBR'][t]))
                print()
                print('AVA: ' + str(F['AVAL'][t] + F['AVAR'][t]))
                print('AVD: ' + str(F['AVDL'][t] + F['AVDR'][t]))
                print('AVE: ' + str(F['AVEL'][t] + F['AVER'][t]))
                print()
                fw.append((F['AVBL'][t] + F['AVBR'][t] + F['PVCL'][t] + F['PVCR'][t]) / 4)
                if len(fw) > 10:
                    fw.pop(0)
                print('forward: ' + str(sum(fw) / 10))
                bw.append((F['AVAL'][t] + F['AVAR'][t] + F['AVDL'][t] + F['AVDR'][t] + F['AVEL'][t] + F['AVER'][t]) / 6)
                if len(bw) > 10:
                    bw.pop(0)
                print('backward: ' + str(sum(bw)/10))
                print()

                lw.append(F['AVAL'][t] + F['AVDL'][t] + F['AVEL'][t])
                if len(lw) > 10:
                    lw.pop(0)
                print('lf'+str(sum(lw)/10))
                rw.append(F['AVAR'][t] + F['AVDR'][t] + F['AVER'][t])
                if len(rw) > 10:
                    rw.pop(0)
                print('rf' + str(sum(rw)/10))



                time.sleep(0.001)

            for synapse in synapses:
                synapse.compute(neurons, T[t])

            # Updates the time each 0.01 seconds
            if T[t]*1000 % 1 == 0:
                gui.update_time(T[t])
                gui.update_robot_status(linker.is_connected())
                linker.update_time(T[t])
                linker.enable_robot(gui.is_robot_enabled())

            if gui.get_nose_s_touch():
                neurons['FLPR'].inject_current(5e-12)
                neurons['FLPL'].inject_current(5e-12)
                neurons['ASHL'].inject_current(5e-12)
                neurons['ASHR'].inject_current(5e-12)
                neurons['IL1VL'].inject_current(5e-12)
                neurons['IL1VR'].inject_current(5e-12)
                neurons['OLQDL'].inject_current(5e-12)
                neurons['OLQDR'].inject_current(5e-12)
                neurons['OLQVR'].inject_current(5e-12)
                neurons['OLQVL'].inject_current(5e-12)

            if gui.get_nose_h_touch():
                neurons['FLPR'].inject_current(8e-12)
                neurons['FLPL'].inject_current(8e-12)
                neurons['ASHL'].inject_current(8e-12)
                neurons['ASHR'].inject_current(8e-12)
                neurons['IL1VL'].inject_current(8e-12)
                neurons['IL1VR'].inject_current(8e-12)
                neurons['OLQDL'].inject_current(8e-12)
                neurons['OLQDR'].inject_current(8e-12)
                neurons['OLQVR'].inject_current(8e-12)
                neurons['OLQVL'].inject_current(8e-12)

            if gui.get_l_side_touch():
                neurons['ALML'].inject_current(20e-12)
                neurons['PLML'].inject_current(20e-12)
                neurons['AVM'].inject_current(20e-12)
                neurons['PVDL'].inject_current(20e-12)
                neurons['ADEL'].inject_current(20e-12)
                neurons['PDEL'].inject_current(20e-12)

            if gui.get_r_side_touch():
                neurons['ALMR'].inject_current(20e-12)
                neurons['PLMR'].inject_current(20e-12)
                neurons['AVM'].inject_current(20e-12)
                neurons['PVDR'].inject_current(20e-12)
                neurons['ADER'].inject_current(20e-12)
                neurons['PDER'].inject_current(20e-12)

            neurons['PVDL'].inject_current(20e-12)
            neurons['PVDR'].inject_current(20e-12)
            neurons['PVCL'].inject_current(20e-12)
            neurons['PVCR'].inject_current(20e-12)

            update_counter += 1
            current_time = t

            if not running:
                print ('Connectome simulation STOPPED')
                break

        elapsed_time = time.time() - start_time
        print_statistics(T[t], elapsed_time, len(generators), len(neurons), len(synapses))

    threading.Thread(target=compute).start()

    gui.start()

    linker.compute_axes()

    # After this point, the GUI is closed, meaning the program should end
    linker.stop()  # Stops connection with robot worm
    linker.join()  # Waits till linker thread stops
    running = False  # Stops simulation thread


def print_statistics(simulation_time, elapsed_time, n_generators, n_neurons, n_synapses):
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


def plot_response(_event, key):
    global current_time
    matlab.figure(num=key)

    print("GUI: Showing Plot Response for Neuron: " + key)

    v_plot = matlab.subplot(3, 1, 1)
    matlab.plot(T, V[key])
    matlab.xlabel('Time[s]')
    matlab.ylabel('Voltage[V]')
    v_plot.set_xlim(left=0, right=T[current_time])

    a_plot = matlab.subplot(3, 1, 2)
    matlab.plot(T, I[key], color='orange')
    matlab.xlabel('Time[s]')
    matlab.ylabel('Current[A]')
    a_plot.set_xlim(left=0, right=T[current_time])

    f_plot = matlab.subplot(3, 1, 3)
    matlab.plot(T, F[key], color='green')
    matlab.xlabel('Time[s]')
    matlab.ylabel('Frequency[Hz]')
    f_plot.set_xlim(left=0, right=T[current_time])

    matlab.show()


if __name__ == '__main__':
    main()
