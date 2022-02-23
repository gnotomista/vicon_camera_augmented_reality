from OpenCVYaml import OpenCVYamlReader
import cv2
import numpy as np
from os import path

class FunstuffsCam:

    def __init__(self):
        self.yml_reader = OpenCVYamlReader()

        with open(path.dirname(__file__)+'/../config/calibration_funstuffs_cam.yml') as file_in:
            result = self.yml_reader.load_opencv_yaml(file_in.read())
        self.K = result['camera_matrix']
        self.d = result['distortion_coefficients']

        with open(path.dirname(__file__)+'/../config/qr_vicon_world_Npoints.yml') as file_in:
            result = self.yml_reader.load_opencv_yaml(file_in.read())
        self.world_points = result['world_positions']

        with open(path.dirname(__file__)+'/../config/qr_vicon_image_Npoints.yml') as file_in:
            result = self.yml_reader.load_opencv_yaml(file_in.read())
        self.image_points = result['image_positions']

        _, self.R, self.t = cv2.solvePnP(self.world_points, self.image_points, self.K, self.d)

    def project_point(self, world_point):
        image_point, _ = cv2.projectPoints(world_point, self.R, self.t, self.K, self.d)
        return image_point[0][0]
