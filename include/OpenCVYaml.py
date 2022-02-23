from os import linesep
from numpy import array
import yaml
import cv2

class OpenCVYamlReader:

    def __init__(self):
        yaml.add_constructor(u"tag:yaml.org,2002:opencv-matrix", self.opencv_matrix)

    def opencv_matrix(self, loader, node):
        mapping = loader.construct_mapping(node, deep=True)
        mat = array(mapping["data"])
        mat.resize(mapping["rows"], mapping["cols"])
        return mat

    def load_opencv_yaml(self, c):
        wicked_legacy = "%YAML:1.0"
        if c.startswith(wicked_legacy):
            c = "%YAML 1.1" + linesep + "---" + c[len(wicked_legacy):]
        return yaml.load(c)

class OpenCVYamlWriter:

    def __init__(self, file_name):
        self.file_name = file_name
        self.fs = cv2.FileStorage(self.file_name, cv2.FILE_STORAGE_WRITE)

    def write(self, var_name, data):
        self.fs.write(var_name, data)

    def release(self):
        self.fs.release()
        with open(self.file_name, 'r+') as file_in:
            lines = file_in.readlines()
            file_in.seek(0)
            file_in.writelines("%YAML:1.0")
            file_in.writelines(linesep)
            file_in.writelines(lines[2:])
            file_in.truncate()
