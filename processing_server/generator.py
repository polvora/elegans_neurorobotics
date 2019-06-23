class PulseGenerator(object):
    def __init__(self, delay_time, duration_time, current, target):
        self.delay_time = delay_time
        self.duration_time = duration_time
        self.current = current
        self.simulation_time = self.delay_time + self.duration_time
        self.target = target

        self.last_current = 0

    def __str__(self):
        return "GENERATOR (Pulse): Delay: " + str(self.delay_time) + "[s] ; Duration: " + str(self.duration_time) + \
               "[s] ; Current: " + str(self.current) + "[A] ; Target: " + str(self.target)

    def get_last_current(self):
        return self.last_current

    def compute(self, neurons, time):
        if time > self.simulation_time:
            instant_current = 0
        elif time > self.delay_time:
            instant_current = self.current
        else:
            instant_current = 0
        neurons[self.target].inject_current(instant_current)
        self.last_current = instant_current
        return instant_current

    def get_simulation_time(self):
        return self.simulation_time

    def get_target(self):
        return self.target
