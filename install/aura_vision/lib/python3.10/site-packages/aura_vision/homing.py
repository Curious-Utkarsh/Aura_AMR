import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, Imu, LaserScan
import cv2
from cv_bridge import CvBridge
import numpy as np
from tf_transformations import euler_from_quaternion

class HomingNode(Node):
    def __init__(self):
        super().__init__("homing_node")
        self.img_bridge = CvBridge()
        self.frame = None
        self.markerDetect = False
        self.yaw = 0.0
        self.orient = False
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.cam_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
        self.imu_sub = self.create_subscription(Imu, "/imu/out", self.imu_callback, 10)

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
        # print(self.yaw)


    def camera_callback(self, img):
        self.frame = self.img_bridge.imgmsg_to_cv2(img, 'bgr8')
        if self.frame is not None:
            center_aruco_list, id_list = self.detect_aruco_pose(self.frame)
            for i in range(0, len(id_list)):
                # print(id_list[i])
                if id_list[i] == 'obj_23': #Marker 0

                    center_x = int(center_aruco_list[i][0]) #x
                    center_y = int(center_aruco_list[i][1]) #y

                    cv2.circle(self.frame, (320, 240), radius=5, color=(255, 0, 0), thickness=-1)
                    cv2.circle(self.frame, (center_x, center_y), radius=7, color=(255, 0, 0), thickness=2)

                    self.markerDetect = True

        cv2.imshow('Frame', self.frame)
        cv2.waitKey(1)

        if self.markerDetect == False:
            self.velocity_publisher(-0.1, 0.0)
        else:
            yaw = round(self.yaw, 2)
            print("yaw", yaw)
            if yaw <=  3.0 and self.orient == False:
                self.velocity_publisher(0.0, 0.6)
            else:
                self.velocity_publisher(0.0, 0.0)
                self.orient = True


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
    
def main(args=None):
    rclpy.init(args=args)
    node = HomingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()