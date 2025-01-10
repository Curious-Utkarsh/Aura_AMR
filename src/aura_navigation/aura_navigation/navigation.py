#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class Navigation(Node):
    def __init__(self):
        super.__init__("waypoint_follower_node")


def main(args=None):
    rclpy.init(args=args)
    navNode = Navigation()
    rclpy.spin(navNode)
    navNode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()