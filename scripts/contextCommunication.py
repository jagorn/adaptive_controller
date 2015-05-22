#!/usr/bin/env python
import gringoParser
from adaptive_controller.msg import *


class ContextCommunication:

    __in_topic = '/context/input'
    __out_topic = '/context/model'
    __in_message = ContextInput
    __out_message = ContextModel

    @property
    def in_topic(self):
        return self.__in_topic

    @property
    def out_topic(self):
        return self.__out_topic

    @property
    def in_message(self):
        return self.__in_message

    @property
    def out_message(self):
        return self.__out_message

    def atoms_values2in_message(self, atoms2values):
        message = self.__in_message()
        message.atoms = []
        message.values = []
        for atom, value in atoms2values.iteritems():
            message.atoms.append(atom.__str__())
            message.values.append(value)
        return message

    def in_message2atoms_values(self, message):
        atoms = map(gringoParser.string2fun, message.atoms)
        values = message.values
        atoms2values = {}
        for atom, value in zip(atoms, values):
            atoms2values[atom] = value
        return atoms2values

    def atoms2out_message(self, atoms):
        message = self.__out_message()
        message.atoms = []
        for atom in atoms:
            message.atoms.append(atom.__str__())
        return message

    def out_message2atoms(self, message):
        atoms = map(gringoParser.string2fun, message.atoms)
        return atoms