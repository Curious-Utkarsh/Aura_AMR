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
from rclpy.action import ActionClient
from aura_msgs.action import AuraTask

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
        self.arm_goal_done = 0
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
        self.color_left = 0.0
        self.width = 0
        self.color_right = 0.0
        self.task = 0
        self.complete = False
        self.goal_success = False
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.cam_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
        self.imu_sub = self.create_subscription(Imu, "/imu/out", self.imu_callback, 10)
        self.lidar_sub = self.create_subscription(LaserScan, "/scan", self.lidar_callback, 10)
        self.battety_sub = self.create_subscription(Bool, "/battery_status", self.battery_callback, 10)
        self._action_client = ActionClient(self, AuraTask, '/task_server')

    def send_goal(self, task_number):
        if not self._action_client.server_is_ready():
            self.get_logger().warn('Action server not ready yet. Waiting...')
            return

        # Create a goal message
        goal_msg = AuraTask.Goal()
        goal_msg.task_number = task_number  # Replace with the desired task number

        self.get_logger().info(f'Sending goal with task_number: {goal_msg.task_number}')

        # Send the goal
        future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info(f'Received feedback: {feedback.feedback}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected by the server.')
            return

        self.get_logger().info('Goal accepted by the server.')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info(f'Goal succeeded with result: {result}')
            self.goal_success = True
        else:
            self.get_logger().error(f'Goal failed with result: {result}')

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

    def detect_objects(self, frame, color):
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define HSV range for the color red
        lower_red1 = np.array([0, 120, 70])  # Lower range for red
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])  # Upper range for red
        upper_red2 = np.array([180, 255, 255])

        # Define HSV range for the color blue
        lower_blue = np.array([100, 150, 70])  # Lower range for blue
        upper_blue = np.array([140, 255, 255])  # Upper range for blue

        # Create mask for blue
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        # Create masks for red
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

        # Combine both masks
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Apply some morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

        # Find contours in the mask
        if color == "RED":
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around detected red objects
        for contour in contours:
            if cv2.contourArea(contour) > 300:  # Filter by area
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box
                cv2.putText(frame, str(color+" Object"), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                self.color_left = x
                self.color_right = x+w
                self.width = w
                cv2.circle(frame, (self.color_left, y), radius=7, color=(255, 0, 0), thickness=2)
                cv2.circle(frame, (self.color_right, y), radius=7, color=(255, 0, 0), thickness=2)
                cv2.circle(frame, (int((self.color_left + self.color_right) / 2.0), y), radius=7, color=(0, 255, 0), thickness=2)
                cv2.circle(frame, (320, y), radius=7, color=(255, 255, 255), thickness=2)
                
        return frame

    def follow_color(self, color):
        if color == "RED":
            center_color = (self.color_left + self.color_right)/2.0
            error = 320 - int(center_color)
            print("error :",error*0.002)
            print("width:", self.width)
            if self.width >= 25 and self.width < 40:
                if self.task == 0:
                    self.send_goal(0)
                    self.task = 1
                elif self.task == 2:
                    self.goal_success = False
                    self.send_goal(2)
                    self.task = 3
                    
            if self.width >= 80:
                self.velocity_publisher(0.0, 0.0)
                self.arm_goal_done = 2
                if self.goal_success == True and self.task == 1:
                    self.send_goal(1)
                    self.task = 2
                if self.goal_success == True and self.task == 3:
                    self.set_goal(2.0, 0.0, 2.5) #EATLIER WAS !.57
                    self.goal_done = False
                    self.task = 4
                    self.goal_success = False
            else:
                self.velocity_publisher(0.2, error*0.002)

        if color == "BLUE":
            #print("Entered BLUE")
            center_color = (self.color_left + self.color_right)/2.0
            error = 320 - int(center_color)
            print("error :",error*0.001)
            #print("width:", self.width)
            if self.width >= 45 and self.width < 75:
                if self.task == 4:
                    self.send_goal(3)
                    self.task = 5
                elif self.task == 6:
                    self.goal_success = False
                    #PUT SET GOAL HERE FOR NEXT DUSTBIN
                    self.set_goal(-8.7, 0.0, 1.0)
                    self.goal_done = False
                    self.send_goal(5)
                    self.task = 2 #DONE PURPOSELY
                    self.complete = True
                    
            if self.width >= 80:
                self.velocity_publisher(0.0, 0.0)
                self.arm_goal_done = 2
                if self.goal_success == True and self.task == 5:
                    self.send_goal(4)
                    self.task = 6
                if self.goal_success == True and self.task == 7:
                    self.task = 8
            else:
                self.velocity_publisher(0.2, error*0.001)

        
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
            if self.task < 4:
                self.frame = self.detect_objects(self.frame, "RED")
            if self.task >= 4:
                if self.task == 4 and self.complete == True:
                    self.task = 8
                self.frame = self.detect_objects(self.frame, "BLUE")
            if self.task == 8:
                self.send_goal(6)
                self.arm_goal_done = 1 #GO BACK TO DOCK
                self.goal_done = True
                self.battery_low = True
                self.task = 9

                #ADDED TO PREVENT COMING OUT OF DOCK
                # self.in_dock = False
                # self.battery_low = False
                # self.orient = True
                # self.goal_done = False

            #print(self.task)

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
                        self.set_goal(2.0, 1.5, 0.0) #Docking Start Posn.
                    else:
                        #self.random_obstacle_avoidance()
                        if self.task < 4:
                            self.follow_color("RED")
                        if self.task >= 4:
                            self.follow_color("BLUE") 
            

        if self.goal_done == True and self.arm_goal_done == 1: #Go Back to Dock
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


    def set_goal(self, x,y,z):
        self.nav.waitUntilNav2Active()

        goal_pose = self.create_pose_stamped(x,y,z) #Align with dock but 3 cells back from it

        waypoint = [goal_pose]
        self.nav.followWaypoints(waypoint)

        while not self.nav.isTaskComplete(): 
            feedback = self.nav.getFeedback()
            print(feedback)

        print(self.nav.getResult())
        self.goal_done = True
        print("Reached Goal!!")

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