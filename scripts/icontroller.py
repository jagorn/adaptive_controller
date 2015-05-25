#!/usr/bin/env python
import rospy


class ROSoClingo:

    Time = 1

    Sent_messages = []
    Received_messages = []

    def __init__(self, handle_request, handle_solver, handle_communication, handle_context):
        handle_solver.start(self.get_time, self.check_time, handle_request.handle_goal, handle_communication.send_message)
        handle_communication.start(self.get_time, self.add_send, self.add_receive, handle_solver.set_externals)
        handle_request.start(self.get_time, handle_solver.set_externals)
        handle_context.start(handle_solver.set_externals)

    def add_send(self, message):
        is_new = True
        for sent in self.Sent_messages:
            if message.id == sent.id:
                is_new = False
        if is_new:
            self.Sent_messages.append(message)

    def add_receive(self, message):
        is_new = True
        for sent in self.Received_messages:
            if message.id == sent.id:
                is_new = False
        if is_new:
            self.Received_messages.append(message)

    def check_time(self):
        is_completed = False

        # ROS log
        log_message = "ROSoClingo - action queue:"
        log_message += "\nsent: "
        for sent in self.Sent_messages:
            log_message += str(sent.id) + ":" + str(sent.action) + " "
        log_message += "\nreceived: "
        for received in self.Received_messages:
            log_message += str(received.id) + ":" + str(received.value) + " "
        log_message += "\ntime = " + self.Time.__str__() + "\n"

        if all(element in self.Received_messages for element in self.Sent_messages) and self.Sent_messages != []:
            is_completed = True

            self.Time += 1
            self.Sent_messages = []
            self.Received_messages = []

            log_message += "cycle completed\n"

        rospy.loginfo(log_message)
        return is_completed

    def get_time(self):
        return self.Time
