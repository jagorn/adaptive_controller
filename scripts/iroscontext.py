#!/usr/bin/env python
import rospy
from contextCommunication import ContextCommunication


class HandleContext:

    __set_external = None
    __context_to_solver = None

    __communication = None
    __context_model = []

    def __init__(self, context_to_solver):
        self.__communication = ContextCommunication()
        self.__context_to_solver = context_to_solver

    def start(self, set_externals):
        self.__set_external = set_externals
        rospy.Subscriber(self.__communication.out_topic, self.__communication.out_message, self.__on_received_context)
        return True

    def __on_received_context(self, message):
        old_context_model = self.__context_model
        self.__context_model = self.__communication.out_message2atoms(message)

        assertions2values = {}

        # remove old assertions which are no more valid
        for atom in old_context_model:
            if atom not in self.__context_model:
                assertions2values[atom] = False

        # add new assertions which were not valid before
        for atom in self.__context_model:
            if atom not in old_context_model:
                assertions2values[atom] = True

        # ROS log
        log_message = "ROSoClingo - context received:\n"
        log_message += "old model:\n"
        for atom in old_context_model:
            log_message += atom.__str__() + "\n"
        log_message += "model update:\n"
        for atom, value in assertions2values.iteritems():
            log_message += atom.__str__() + " = " + str(value) + "\n"
        log_message += "new model:\n"
        for atom in self.__context_model:
            log_message += atom.__str__() + "\n"
        rospy.loginfo(log_message)

        self.__set_external(self.__context_to_solver(assertions2values))