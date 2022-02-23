#!/usr/bin/env python
from sys import path
from os import getcwd
path.insert(0, getcwd()+'/../include')
from OpenCVYaml import OpenCVYamlWriter, OpenCVYamlReader
from geometry_msgs.msg import PoseStamped
from time import time
import numpy as np
import rospy
import cv2

class VrpnListener:
    def __init__(self):
        self.current_position = None
        self.positions = np.zeros(shape=(0,3))

    def store_pose(self, msg):
        self.current_position = np.asarray([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])

    def run(self):
    	rospy.init_node('vrpn_grabber', anonymous=True)
        rospy.Subscriber("/vrpn_client_node/qr_vicon/pose", PoseStamped, self.store_pose)

print 'Waiting 5 seconds pause before starting...'
rospy.sleep(5) # pause 5 seconds before starting
print '...done'

print 'Starting camera...'
# video_source = '../data/extrinsic_calibration_video.avi'
video_source = 0  # camera index
video_reader = cv2.VideoCapture(video_source)
print '...done'

print 'Starting VRPN listener...'
vl = VrpnListener()
vl.run()
print '...done'

last_recorded_frame_time = time()
cv2.namedWindow("frame")
rate = rospy.Rate(30)
n = 0
while not rospy.is_shutdown():

    _, frame = video_reader.read()

    if frame is None:
        break
    else:
        # frame_resized = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        # cv2.imshow("frame", frame_resized)
        cv2.imshow("frame", frame)

    k = cv2.waitKey(1)
    if k == 27:  # ESC
        break
    if time()-last_recorded_frame_time > 3: # record frame every 3 seconds
        n = n + 1
        image_name = '../data/qr_vicon_pics/img_'+str(n)+'.png'
        cv2.imwrite(image_name, frame)
        vl.positions = np.vstack([vl.positions, vl.current_position])
        print 'image', image_name, 'saved and position', vl.positions[-1], 'stored'
        last_recorded_frame_time = time()

    rate.sleep()

file_name = '../config/qr_vicon_world_Npoints.yml'
fs = OpenCVYamlWriter(file_name)
fs.write('world_positions',vl.positions)
fs.release()
print '\nsaved', vl.positions.shape[0], 'images and written', vl.positions.shape[0], 'positions of qr vicon marker to file', file_name

yml_reader = OpenCVYamlReader()
with open(file_name) as file_in:
    result = yml_reader.load_opencv_yaml(file_in.read())
wp = result['world_positions']
print '\nreading test:', wp.shape, '\n', wp
