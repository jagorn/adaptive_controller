#! /usr/bin/env python

import rospy
from contextCommunication import ContextCommunication


def on_received_model(message):

    # ROS log
    log_message = "ContextOutput - output received:\n"
    for atom in message.atoms:
        log_message += atom.__str__() + "\n"
    rospy.loginfo(log_message)


if __name__ == '__main__':
    try:
        rospy.init_node('context_output')

        context = ContextCommunication()
        rospy.Subscriber(context.out_topic, context.out_message, on_received_model)

        # ROS log
        rospy.loginfo("ContextOutput - ready\n")

        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.logerr("program interrupted before completion")