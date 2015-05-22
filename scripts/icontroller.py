#!/usr/bin/env python
import rospy


class ROSoClingo:

    Time = 1

    Send = []
    Received = []

    def __init__(self, handle_request, handle_solver, handle_communication, handle_context):
        handle_solver.start(self.get_time, self.check_time, handle_request.handle_goal, handle_communication.send_message)
        handle_communication.start(self.get_time, self.add_send, self.add_receive, handle_solver.set_externals)
        handle_request.start(self.get_time, handle_solver.set_externals)
        handle_context.start(handle_solver.set_externals)

    def add_send(self, send):
        if send not in self.Send:
            self.Send.append(send)

    def add_receive(self, receive):
        if receive not in self.Received:
            self.Received.append(receive)

    def check_time(self):

        is_completed = False

        # ROS log
        log_message = "ROSoClingo - action queue:\n"
        log_message += "received = " + self.Received.__str__() + "\n"
        log_message += "sent = " + self.Send.__str__() + "\n"
        log_message += "time = " + self.Time.__str__() + "\n"

        if all(element in self.Received for element in self.Send) and self.Send != []:
            is_completed = True

            self.Time += 1
            self.Send = []
            self.Received = []

            log_message += "cycle completed\n"

        rospy.loginfo(log_message)
        return is_completed

    def get_time(self):
        return self.Time
