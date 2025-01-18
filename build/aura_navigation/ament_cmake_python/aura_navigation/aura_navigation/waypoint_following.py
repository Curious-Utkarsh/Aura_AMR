#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations
    
    
class WaypointFollowerNode(Node): 
    def __init__(self):
        super().__init__("waypoint_follower_node") 
        self.nav = BasicNavigator()
        self.set_pose_and_goal()

    def create_pose_stamped(self, position_x, position_y, rotation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, rotation_z)
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.nav.get_clock().now().to_msg()
        goal_pose.pose.position.x = position_x
        goal_pose.pose.position.y = position_y
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.x = q_x
        goal_pose.pose.orientation.y = q_y
        goal_pose.pose.orientation.z = q_z
        goal_pose.pose.orientation.w = q_w
        return goal_pose
        
    def set_pose_and_goal(self):
        # Set Initial Pose (2D Pose Estimator )
        # initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        # self.nav.setInitialPose(initial_pose)

        #Wait for Nav2
        self.nav.waitUntilNav2Active()

        # Create some Nav2 goal poses 
        goal_pose1 = self.create_pose_stamped(0.0, 3.0, 0.0)
        goal_pose2 = self.create_pose_stamped(0.0, 3.0, -1.57)

        # # Go to one pose only
        # self.nav.goToPose(goal_pose1)
        # while not self.nav.isTaskComplete():
        #         #feedback = self.nav.getFeedback()
        #         # print(feedback)
        #         pass

        # Follow Waypoints 
        waypoints = [goal_pose1, goal_pose2]
        self.nav.followWaypoints(waypoints)

        while not self.nav.isTaskComplete(): #waits until all waypoints are covered, ie one cycle is complete.
            feedback = self.nav.getFeedback()
            print(feedback)

        # Get the result 
        print(self.nav.getResult())
    
    
def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollowerNode() 
    rclpy.spin_once(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()