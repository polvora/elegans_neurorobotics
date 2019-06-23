import math


class IaFNeuron(object):
    def __init__(self, tag, resting_potential, threshold_potential,
                 reset_potential, membrane_capacitance, leak_conductance, tau=None):
        self.tag = tag
        self.resting_potential = resting_potential
        self.threshold_potential = threshold_potential
        self.reset_potential = reset_potential
        self.membrane_capacitance = membrane_capacitance
        self.membrane_resistance = 1/leak_conductance
        self.membrane_time_constant = (self.membrane_resistance * self.membrane_capacitance) if tau is None else tau

        self.last_voltage = resting_potential
        self.last_time = 0
        self.last_current = 0

        self.injected_current = 0

        self.fired = 0

    def __str__(self):
        return "NEURON (IaF): Tag: " + str(self.tag) + " ; Resting Potential: " + str(self.reset_potential) + \
               "[V] ; Threshold Potential: " + str(self.threshold_potential) + "[V] ; Reset Potential: " + \
               str(self.reset_potential) + "[V] ; Membrane Capacitance: " + str(self.membrane_capacitance) + \
               "[C] ; Membrane Resistance: " + str(self.membrane_resistance) + "[ohms] ; Membrane Time Constant: " + \
               str(self.membrane_time_constant) + "[s]"

    def inject_current(self, current):
        self.injected_current += current

    def open_channels(self, conductance, e_rev):
        self.injected_current += conductance*(e_rev-self.last_voltage)

    def compute(self, time):
        # Checks if computed twice at the same time, excludes initial time
        assert (time == 0 or self.last_time != time), "Component computed twice at the same time value."
        time_diff = time - self.last_time

        if self.last_voltage > self.threshold_potential:
            instant_voltage = self.reset_potential
            self.fired = True
        else:
            instant_voltage = self.last_voltage + time_diff * \
                              (-(self.last_voltage - self.resting_potential) + self.injected_current *
                               self.membrane_resistance) / self.membrane_time_constant
            # If computed voltage is over threshold it is stored as a spike
            instant_voltage = 0 if instant_voltage > self.threshold_potential else instant_voltage

            self.fired = False

        self.last_voltage = instant_voltage
        self.last_time = time
        self.last_current = self.injected_current
        self.injected_current = 0

        return instant_voltage

    def is_fired(self):
        return self.fired

    def get_last_voltage(self):
        return self.last_voltage

    def get_last_current(self):
        return self.last_current

    def get_tag(self):
        return self.tag

    def get_last_frequency(self):
        return self._get_instant_frequency(self.last_current)

    def _get_instant_frequency(self, current):
        threshold_current = (self.threshold_potential - self.reset_potential)/self.membrane_resistance
        if threshold_current >= current:
            instant_frequency = 0

        else:
            instant_frequency = pow(self.membrane_time_constant * math.log(((
                                        self.membrane_resistance*current) + self.resting_potential -
                                        self.reset_potential)/((self.membrane_resistance*current) +
                                                               self.resting_potential - self.threshold_potential)), -1)

        return instant_frequency
