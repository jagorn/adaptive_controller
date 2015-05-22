#!/usr/bin/env python
import rospy
import rospkg
import gringo
import contextCommunication


class ContextMiddleware:

    __context_source = '/asp/context.lp'
    __communication = None
    __publisher = None
    __solver = None
    __future = None
    __interrupted = None
    __model = []

    def __init__(self):
        self.__communication = contextCommunication.ContextCommunication()

        package = rospkg.RosPack()
        context_path = package.get_path('adaptive_controller') + self.__context_source

        self.__solver = gringo.Control()
        self.__solver.load(context_path)
        self.__solver.ground([("base", [])])

        self.__future = self.__solver.solve_async(None, self.__on_model, self.__on_finish)
        self.__future.wait()

        self.__publisher = rospy.Publisher(self.__communication.out_topic, self.__communication.out_message, latch=True, queue_size=10)
        rospy.Subscriber(self.__communication.in_topic, self.__communication.in_message, self.__on_received_context)

    def __on_received_context(self, input_msg):

        # ROS log
        log_message = "ContextMiddleware - input received:\n"

        self.__future.interrupt()
        atoms2values = self.__communication.in_message2atoms_values(input_msg)
        for atom, value in atoms2values.iteritems():
            self.__solver.assign_external(atom, value)
            log_message += str(atom) + " = " + str(value) + "\n"
        rospy.loginfo(log_message)

        self.__interrupted = True
        self.__model = []
        self.__future = self.__solver.solve_async([], self.__on_model, self.__on_finish)
        if self.__future.get() == gringo.SolveResult.SAT and self.__interrupted is False:
            self.__publish_context()

    def __on_model(self, model):
        self.__model[:] = model.atoms(gringo.Model.SHOWN)

    def __on_finish(self, result, interrupted):
        self.__interrupted = interrupted

    def __publish_context(self):
        context_msg = self.__communication.atoms2out_message(self.__model)
        self.__publisher.publish(context_msg)

        # ROS log
        log_message = "ContextMiddleWare - model published:\n"
        for atom in self.__model:
            log_message += atom.__str__() + "\n"
        rospy.loginfo(log_message)