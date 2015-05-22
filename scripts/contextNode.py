#!/usr/bin/env python
import rospy
import contextMiddleware

rospy.init_node('contextMiddleware')
reasoner = contextMiddleware.ContextMiddleware()

# ROS log
rospy.loginfo('contextMiddleware ready\n')

rospy.spin()
