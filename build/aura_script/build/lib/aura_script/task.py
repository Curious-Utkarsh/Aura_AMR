import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import Image, Imu, LaserScan
import cv2
from cv_bridge import CvBridge
import numpy as np
from tf_transformations import euler_from_quaternion, quaternion_from_euler
from nav2_simple_commander.robot_navigator import BasicNavigator
import multiprocessing 
from std_msgs.msg import Bool
import random
import math


class TaskNode(Node):
    def __init__(self):
        super().__init__("task_node")
        self.img_bridge = CvBridge()
        self.nav = BasicNavigator()
        self.frame = None
        self.markerDetect = False
        self.yaw = 0.0
        self.orient = False
        self.goal_done = False
        self.in_dock = True
        self.phase_1 = False
        self.flag = True
        self.dock_found = False
        self.front_ray = 0.0
        self.left_ray = 0.0
        self.right_ray = 0.0
        self.dock_threshold = 0.2
        self.battery_low = False
        self.obstacle_avoid_threshold = 1.5
        self.turn_taking = False
        self.turn_taken = False
        self.turn_right = False
        self.decision_made = False
        self.start_bot = False
        self.change_dir = -1
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.cam_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
        self.imu_sub = self.create_subscription(Imu, "/imu/out", self.imu_callback, 10)
        self.lidar_sub = self.create_subscription(LaserScan, "/scan", self.lidar_callback, 10)
        self.battety_sub = self.create_subscription(Bool, "/battery_status", self.battery_callback, 10)

    def battery_callback(self, battery_status):
        self.battery_low = battery_status.data

    def velocity_publisher(self, x, z):
        vel = Twist()
        vel.linear.x = x
        vel.angular.z = z
        self.vel_pub.publish(vel)

    def imu_callback(self, imu):
        orientation = imu.orientation
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        roll, pitch, yaw = euler_from_quaternion([x,y,z,w])
        self.yaw = yaw # rotation about z-axis
        # print("Yaw :", self.yaw)

    def lidar_callback(self, scan):
        self.front_ray = min(scan.ranges[1], 100)  
        self.right_ray = min(scan.ranges[330], 100)
        self.left_ray = min(scan.ranges[30], 100)

        # print("Right Ray :", self.right_ray)
        # print("Front Ray :", self.front_ray)
        # print("Left Ray :", self.left_ray)
        # print("- - - - - -")
        
    def camera_callback(self, img):
        self.frame = self.img_bridge.imgmsg_to_cv2(img, 'bgr8')
        self.markerDetect = False
        if self.frame is not None:
            center_aruco_list, id_list = self.detect_aruco_pose(self.frame)
            for i in range(0, len(id_list)):
                # print(id_list[i])
                if id_list[i] == 'obj_23': #Marker 0

                    center_x = int(center_aruco_list[i][0]) #x
                    center_y = int(center_aruco_list[i][1]) #y

                    cv2.circle(self.frame, (320, 240), radius=5, color=(255, 0, 0), thickness=-1)
                    cv2.circle(self.frame, (center_x, center_y), radius=7, color=(255, 0, 0), thickness=2)
                    error = 320 - center_x #Error in Alignment

                    self.markerDetect = True

        cv2.imshow('Frame', self.frame)
        cv2.waitKey(1)

        #Coming Out of Dock
        if self.markerDetect == False and self.in_dock == True and self.phase_1 == False: #Come Out of Dock
            self.velocity_publisher(-0.1, 0.0)
            print("Coming Out of Dock!!")
        else:
            yaw = round(self.yaw, 2)
            # print("yaw", yaw)
            if yaw <=  3.0 and self.orient == False:
                self.phase_1 = True
                self.velocity_publisher(0.0, 0.6)
                print("Taking Turn For Journey!!")
            else:
                self.velocity_publisher(0.0, 0.0)
                self.orient = True
                self.in_dock = False
                if self.goal_done == False:
                    # print("Going on Journey!!")
                    if self.battery_low == True:
                        self.set_goal() # Go to Goal Pose
                    else:
                        #self.random_obstacle_avoidance()
                        #self.coverage_algorithm()
                        self.arm_goals()

        if self.goal_done == True: #Go Back to Dock
            thres_front = 0.8
            thres_side = 1.5
            #Going Back of Dock
            if self.markerDetect == False:
                if (self.front_ray > thres_front)  and (self.right_ray > thres_side or self.left_ray > thres_side):
                    vel_x = 0.0
                    vel_z = -self.yaw/4.0
                    print("Searching Dock!!")
                else:
                    vel_x = 0.08
                    vel_z = -self.yaw/5.0
                    print("Docking!!")

                if abs(self.yaw) < 0.2 and self.front_ray < self.dock_threshold and self.right_ray < self.dock_threshold and self.left_ray < self.dock_threshold:
                    vel_x = 0.0
                    vel_z = 0.0
                    self.in_dock = True
                    self.orient = False
                    self.markerDetect = False
                    self.goal_done = False
                    self.phase_1 = False
                    self.start_bot = False
                    self.battery_low = False
                    print("Docked Successfully!!")
            else:
                vel_x = 0.08
                vel_z = float(error/100.0)
                # print(vel_z)
                print("Aligning To Dock!!")
 
            self.velocity_publisher(vel_x, vel_z)

    def set_goal(self):
        self.nav.waitUntilNav2Active()

        goal_pose1 = self.create_pose_stamped(0.0, 0.0, 0.0) #Map posn goes there (dock at 2,5)
        goal_pose2 = self.create_pose_stamped(2.0, 1.5, 1.57) #Align with dock but 3 cells back from it

        waypoints = [goal_pose2]
        self.nav.followWaypoints(waypoints)

        while not self.nav.isTaskComplete(): 
            feedback = self.nav.getFeedback()
            print(feedback)

        print(self.nav.getResult())
        self.goal_done = True
        print("Journey Done!!")

    def random_obstacle_avoidance(self):
        if self.front_ray < self.obstacle_avoid_threshold or self.left_ray < self.obstacle_avoid_threshold or self.right_ray < self.obstacle_avoid_threshold:
            print("OBSTACLE DETECTED")
            if self.turn_taking == False:
                imu_current_yaw = self.yaw
                self.turn_taking == True

            if self.decision_made == False:
                if self.left_ray > self.right_ray:
                    print("TAKE LEFT TURN")
                    self.turn_right = False
                elif self.right_ray > self.left_ray:
                    print("TAKE RIGHT TURN")
                    self.turn_right = True
                else:  # Equal distances, pick randomly
                    self.turn_right = random.choice([True, False])
                    print("EQUAL DISTANCES, RANDOMLY CHOSEN:", "RIGHT" if self.turn_right else "LEFT")

                self.decision_made = True
                self.turn_taken = False


            if self.turn_taken == False:
                if self.turn_right == False:
                    if (abs(imu_current_yaw) - abs(self.yaw)) < 1.57:
                        print("TAKING TURN")
                        vel_x = 0.0
                        vel_z = 0.8
                    else:
                        print("LEFT TURN TAKEN")
                        self.turn_taken = True
                        self.turn_taking = False
                        self.decision_made = False
                        self.turn_right = False

                else:
                    if (abs(imu_current_yaw) - abs(self.yaw)) < 1.57:
                        print("TAKING TURN")
                        vel_x = 0.0
                        vel_z = -0.8
                    else:
                        print("RIGHT TURN TAKEN")
                        self.turn_taken = True
                        self.turn_taking = False
                        self.decision_made = False
                        self.turn_right = False
        else:
            print("MOVING FORWARD")
            vel_x = 0.4
            vel_z = 0.0

        self.velocity_publisher(vel_x, vel_z)

    def coverage_algorithm(self):
        # NOT WORKING, THIS ALGO IS NOT TAKING OPPOSITE TURN!, FIX IT LATER WHEN REQUIRED.
        if (
            self.front_ray < self.obstacle_avoid_threshold or 
            self.left_ray < self.obstacle_avoid_threshold or 
            self.right_ray < self.obstacle_avoid_threshold
        ):
            if not self.turn_taking:
                print("OBSTACLE DETECTED")
                self.imu_current_yaw = self.yaw  # Store the current yaw
                self.turn_taking = True         # Mark turn-taking as in progress
                self.turn_taken = False         # Reset turn taken status

            if not self.turn_taken:
                # Calculate the yaw difference
                yaw_diff = abs(self.yaw - self.imu_current_yaw)
                print(yaw_diff)

                if yaw_diff < math.pi:  # Turn until 180-degree rotation
                    print("TAKING --- TURN")
                    vel_x = 0.0
                    vel_z = self.change_dir * 0.8  # Rotate in the change direction
                else:
                    print("TURN TAKEN")
                    self.change_dir *= -1         # Reverse direction for the next obstacle
                    self.turn_taken = True        # Mark turn as completed
                    self.turn_taking = False      # Reset turn-taking flag
        else:
            print("MOVING FORWARD")
            vel_x = 0.4
            vel_z = 0.0

        # Publish the velocity command
        self.velocity_publisher(vel_x, vel_z)

    def arm_goals(self):
        self.nav.waitUntilNav2Active()

        goal_pose_red = self.create_pose_stamped(2.0, 1.5, 0.0) #Red Bar
        #goal_pose2 = self.create_pose_stamped(2.0, 1.5, 1.57) #Align with dock but 3 cells back from it

        waypoints = [goal_pose_red]
        self.nav.followWaypoints(waypoints)

        while not self.nav.isTaskComplete(): 
            feedback = self.nav.getFeedback()
            print(feedback)

        print(self.nav.getResult())
        self.goal_done = True
        print("Arrived at Red Bar")

        
    def detect_aruco_pose(self, img):
        marker_size = 0.60  #0.30
        axis_size = 0.3 #0.15

        center_aruco_list = []
        id_list = []

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        aruco_params = cv2.aruco.DetectorParameters()

        cam_mat = np.array([[931.1829833984375, 0.0, 640.0], [0.0, 931.1829833984375, 360.0], [0.0, 0.0, 1.0]])
        dist_mat = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray_img, aruco_dict, parameters=aruco_params)

        if len(corners) > 0:
            ids = ids.flatten()
            for i in range(len(ids)):
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], marker_size, cam_mat, dist_mat)
                cv2.aruco.drawDetectedMarkers(img, corners)
                cv2.drawFrameAxes(img, cam_mat, dist_mat, rvec, tvec, axis_size)

                center_x = int((corners[i][0][0][0] + corners[i][0][2][0]) / 2.0)
                center_y = int((corners[i][0][0][1] + corners[i][0][2][1]) / 2.0)
                center_aruco_list.append((center_x, center_y))
                id_list.append(f'obj_{ids[i]}')

        return center_aruco_list, id_list
    
    def create_pose_stamped(self, position_x, position_y, rotation_z):
        q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, rotation_z)
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
    
def main(args=None):
    rclpy.init(args=args)
    node = TaskNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()