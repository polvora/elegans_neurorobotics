import math


class TwoExpSynapse(object):
    def __init__(self, g_max, rise_time, decay_time, e_rev, weight, pre_neuron, post_neuron, simulation_time):
        self.e_rev = e_rev
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron

        self.g_max = g_max
        self.rise_time = rise_time
        self.decay_time = decay_time
        self.weight = weight
        self.simulation_time = simulation_time

        peak_time = math.log(decay_time / rise_time) * (rise_time * decay_time) / (decay_time - rise_time)
        self.waveform_factor = 1/(-math.exp(-peak_time/rise_time)+math.exp(-peak_time/decay_time))

        self.synapses_t0 = list()

        self.last_time = 0

    def __str__(self):
        return "SYNAPSE (Two Exponential): Max Conductance: " + str(self.g_max) + "[S] ; Rise Time: " + \
               str(self.rise_time) + "[s] ; Decay Time: " + str(self.decay_time) + "[s] ; Reversal Potential: " + \
               str(self.e_rev) + "[V] ; Weight: " + str(float(self.weight)) + " ; Pre-synaptic Neuron Tag: " + \
               self.pre_neuron + " ; Post-synaptic Neuron Tag: " + self.post_neuron + " ; Simulation Time: " + \
               str(self.simulation_time) + "[s]"

    def get_presynaptic_neuron(self):
        return self.pre_neuron

    def get_postsynaptic_neuron(self):
        return self.post_neuron

    def compute(self, neurons, time):
        # Checks if computed twice at the same time, excludes initial time
        assert (time == 0 or self.last_time != time), "Component computed twice at the same time value."
        if neurons[self.pre_neuron].is_fired():
            self.synapses_t0.append(time)  # Stores the initial time of a synapse

        # Computes the conductance and applies it to post synaptic neuron
        t0_aux = list()
        for t0 in self.synapses_t0:
            if (time-t0) < self.simulation_time:
                g = self._get_conductance(t0, time)
                neurons[self.post_neuron].open_channels(g, self.e_rev)
                t0_aux.append(t0)

        # Reconstruct the list with synapses that are inside the simulation time only
        self.synapses_t0 = t0_aux

        self.last_time = time

    def _get_conductance(self, t0, t):
        return self.g_max*self.weight*self.waveform_factor*(math.exp(-(t-t0)/self.decay_time)-math.exp(-(t-t0) /
                                                                                                       self.rise_time))


class GapJunction(object):
    def __init__(self, g, weight, pre_neuron, post_neuron):
        self.g = g
        self.weight = weight
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron

        self.last_time = 0

    def __str__(self):
        return "SYNAPSE (Gap Junction): Conductance: " + str(self.g) + "[S] ; Weight: " + str(self.weight) + \
               " ; Pre-synaptic Neuron Tag: " + self.pre_neuron + " ; Post-synaptic Neuron Tag: " + self.post_neuron

    def compute(self, neurons, time):
        # Checks if computed twice at the same time, excludes initial time
        assert (time == 0 or self.last_time != time), "Component computed twice at the same time value."
        pre_voltage = neurons[self.pre_neuron].get_last_voltage()
        post_voltage = neurons[self.post_neuron].get_last_voltage()

        pre_current = self.weight * self.g * (post_voltage - pre_voltage)
        post_current = self.weight * self.g * (pre_voltage - post_voltage)

        neurons[self.pre_neuron].inject_current(pre_current)
        neurons[self.post_neuron].inject_current(post_current)

        self.last_time = time

    def get_presynaptic_neuron(self):
        return self.pre_neuron

    def get_postsynaptic_neuron(self):
        return self.post_neuron

    def get_conductance(self):
        return self.g
