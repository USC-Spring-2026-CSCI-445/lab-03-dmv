#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math


class TurtlebotController:

    def __init__(self):
        rospy.init_node("turtlebot_controller", anonymous=True)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.rate = rospy.Rate(10)  # 10 Hz
        rospy.sleep(1)

        # Motion parameters
        self.linear_speed = 0.2      # m/s
        self.angular_speed = 0.5     # rad/s
        self.side_length = 0.30      # meters (30 cm)

    def publish_twist(self, move_cmd, duration):
        end_time = rospy.Time.now() + rospy.Duration(duration)
        while rospy.Time.now() < end_time and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(move_cmd)
            self.rate.sleep()

    def stop_turtlebot(self):
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.0
        self.publish_twist(move_cmd, 1)

    def move_forward(self):
        print("Moving forward 30 cm...")
        move_cmd = Twist()
        move_cmd.linear.x = self.linear_speed
        move_cmd.angular.z = 0.0

        duration = self.side_length / self.linear_speed  # 0.30 / 0.2 = 1.5 s
        self.publish_twist(move_cmd, duration)

    def turn_left_90(self):
        print("Turning left 90 degrees...")
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = self.angular_speed

        duration = (math.pi / 2) / self.angular_speed
        self.publish_twist(move_cmd, duration)

    def move_square(self):
        for _ in range(4):
            self.move_forward()
            self.turn_left_90()

        self.stop_turtlebot()


def main():
    controller = TurtlebotController()
    try:
        controller.move_square()
    except rospy.ROSInterruptException:
        pass


if __name__ == "__main__":
    main()
