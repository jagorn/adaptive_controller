#! /usr/bin/env python
import rospy
from rosoclingoCommunication import RosoclingoCommunication

__communication = RosoclingoCommunication()
__topic = rospy.Publisher(__communication.in_topic, __communication.in_message, latch=True, queue_size=10)


def __on_action_request(message):
    feedback_msg = __communication.in_message()
    feedback_msg.id = message.id
    feedback_msg.value = "success"
    rospy.sleep(2.5)
    __topic.publish(feedback_msg)

    # ROS log
    rospy.loginfo("ActionsFulfiller - action %s executed successfully\n", message.id)


rospy.init_node('ActionsFulfiller')
rospy.Subscriber(__communication.out_topic, __communication.out_message, __on_action_request)

# ROS log
rospy.loginfo("ActionsFulfiller - ready\n")

rospy.spin()
