#!/usr/bin/env python
import rospy
import sys
from gringo import Fun
import gringoParser
from rosoclingoCommunication import RosoclingoCommunication
import icontroller
import iroshandler
import iroscontext


def separate_parameter(inlist):
    list = []
    arguments = []
    for element in inlist:
        if element == "--files:":
            arguments = list
            list = []
        else:
            list.append(element)
    return (arguments,list)


def goal_to_solver(id, request, time):
    return {Fun("_request", [id, gringoParser.string2fun(request), time]): True}


def cancel_to_solver(id, time):
    return {Fun("_cancel", [id, time]): True}


def message_to_solver(message, time):
    return {Fun("_value", [gringoParser.string2fun(message.id), gringoParser.string2fun(message.value), time]): True}


def context_to_solver(assertions2values):
    context = {}
    for assertion, value in assertions2values.iteritems():
        context_assertion = Fun("_context", [assertion])
        context[context_assertion] = value
    return context


def solver_to_message(id, action):
    message = handler.out_message()
    message.id = str(id)
    message.action = str(action)
    return message

# ROS part
rospy.init_node('ROSoClingo', argv=sys.argv, anonymous=True)
(arguments, files) = separate_parameter(rospy.myargv(sys.argv[1:]))
handler = RosoclingoCommunication()
publisher = rospy.Publisher(handler.out_topic, handler.out_message, latch=True, queue_size=10)
handle_communication = iroshandler.HandleCommunication(publisher, handler.in_topic, handler.in_message, message_to_solver)
handle_request = iroshandler.HandleRequest(handler.action_topic, handler.action, goal_to_solver, cancel_to_solver)
handle_solver = iroshandler.HandleSolver(arguments, files, solver_to_message)
handle_context = iroscontext.HandleContext(context_to_solver)
rosoclingo = icontroller.ROSoClingo(handle_request,handle_solver, handle_communication, handle_context)

# ROS log
rospy.loginfo('ROSoClingo - ready\n')

rospy.spin()
