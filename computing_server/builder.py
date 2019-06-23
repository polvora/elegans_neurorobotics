import xml.etree.ElementTree as Et
from helpers import *
from neuron import *
from generator import *
from synapse import *


class Builder:
    def __init__(self, file_name):
        # Gets the root element of the XML file
        self.nml = Et.parse(file_name).getroot()

        # Strips the schema location from every element tag name
        # https://stackoverflow.com/questions/13412496/python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
        for element in self.nml.iter():
            if '}' in element.tag:
                element.tag = element.tag.split('}', 1)[1]  # strip all namespaces

    def build_neurons(self):
        # Initializes the neurons
        neurons = dict()
        # Stores the network of populations
        network = self.nml.find('network')
        # Stores all populations in the network
        populations = network.findall('population')
        # For each population creates the number of neurons according to its attributes
        for population in populations:
            cell_id = population.attrib['component']
            cell_tag = population.attrib['id']
            # Looks for each children id to find the cell that corresponds the id
            for cell in self.nml:
                if 'id' in cell.attrib and cell.attrib['id'] == cell_id:
                    if cell.tag == 'iafCell':
                        resting_potential = parse_magnitude(cell.attrib['leakReversal'])
                        threshold_potential = parse_magnitude(cell.attrib['thresh'])
                        reset_potential = parse_magnitude(cell.attrib['reset'])
                        membrane_capacitance = parse_magnitude(cell.attrib['C'])
                        leak_conductance = parse_magnitude(cell.attrib['leakConductance'])
                        tau = parse_magnitude(cell.attrib['tau1']) if 'tau1' in cell.attrib else None

                        # Updates new neuron with the obtained parameters
                        neurons.update({cell_tag: IaFNeuron(cell_tag, resting_potential, threshold_potential,
                                                            reset_potential, membrane_capacitance, leak_conductance,
                                                            tau)})
                        break
        return neurons

    def build_generators(self):
        # Initializes the generators
        generators = list()
        # Stores the network
        network = self.nml.find('network')
        # Stores all input lists in the network
        input_lists = network.findall('inputList')
        # For each input list creates the number of generators according to its attributes
        for input_list in input_lists:
            input_id = input_list.attrib['component']
            target = input_list.attrib['population']
            # Looks for each children id to find the generator that corresponds the id
            for generator in self.nml:
                if 'id' in generator.attrib and generator.attrib['id'] == input_id:
                    if generator.tag == 'pulseGenerator':
                        delay_time = parse_magnitude(generator.attrib['delay'])
                        duration_time = parse_magnitude(generator.attrib['duration'])
                        current = parse_magnitude(generator.attrib['amplitude'])

                        # Appends new generator  with the obtained parameters
                        generators.append(PulseGenerator(delay_time, duration_time, current, target))
                        break

        return generators

    def build_synapses(self):
        # Initializes the generators
        synapses = list()
        # Stores the network
        network = self.nml.find('network')
        # Stores all chemical projections in the network
        chemical_projections = network.findall('projection')
        # For each regular projection creates a corresponding synapse object
        for projection in chemical_projections:
            pre_neuron = projection.attrib['presynapticPopulation']
            post_neuron = projection.attrib['postsynapticPopulation']
            synapse_id = projection.attrib['synapse']
            # If not a muscle looks for weight between neurons
            if "muscle" not in synapse_id:
                connection = projection.find('connectionWD')
                weight = parse_magnitude(connection.attrib['weight'])
            else:
                weight = 1

            for synapse in self.nml:
                if 'id' in synapse.attrib and synapse.attrib['id'] == synapse_id:
                    g_max = parse_magnitude(synapse.attrib['gbase'])
                    e_rev = parse_magnitude(synapse.attrib['erev'])
                    tau_decay = parse_magnitude(synapse.attrib['tauDecay'])
                    tau_rise = parse_magnitude(synapse.attrib['tauRise'])

                    # Appends new synapse with the obtained parameters
                    synapses.append(
                        TwoExpSynapse(g_max, tau_rise, tau_decay, e_rev, weight, pre_neuron, post_neuron, 1.1
                                      ))
                    break

        # Stores all the electrical projections in the network
        electrical_projections = network.findall('electricalProjection')
        # For each electrical projection creates a corresponding synapse object
        for projection in electrical_projections:
            pre_neuron = projection.attrib['presynapticPopulation']
            post_neuron = projection.attrib['postsynapticPopulation']

            connection = projection.find('electricalConnectionInstanceW')
            weight = parse_magnitude(connection.attrib['weight'])
            synapse_id = connection.attrib['synapse']

            for synapse in self.nml:
                if 'id' in synapse.attrib and synapse.attrib['id'] == synapse_id:
                    g = parse_magnitude(synapse.attrib['conductance'])

                    synapses.append(GapJunction(g, weight, pre_neuron, post_neuron))
                    break

        return synapses
