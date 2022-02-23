# vicon_camera_augmented_reality
Setup of a Vicon tracking system with a (video) camera for augmented reality applications.

## Setup

### 1. Collect images of the visual marker and its poses in the world frame

#### Requirements
* Vicon system
* A camera looking at the Vicon workspace
* PC with ROS
* vrpn_client_ros package https://github.com/ros-drivers/vrpn_client_ros
* Python libraries: `numpy`, `rospy`, `cv2`
* A *Vicon-visual marker* like the one in figure data/qr_vicon_pics/img_42.png, i.e. 4 Vicon markers mounted at the corners of the Aruco marker with ID 0 of the DICT_4X4_50, so that the center of the Vicon configuration is at the center of the Aruco marker

#### Steps
1. Connect the PC where you run this code to the Vicon switch and set the IP so that you can communicate with the PC where the Vicon tracker runs
2. Connect the PC where you run this code to the camera, and change the value of `video_source` on line 30 of the script `ros/record_qr_vicon.py` to match the one of the camera (on a laptop: 0 is usually the built-in webcam, 1, 2, etc. are assigned sequentially to cameras that are connected once the PC is switched on)
3. Start the Vicon tracker software and define the object as *qr_vicon*
4. Run `roslaunch vrpn_client_ros sample.launch server:=192.168.viconserver.ipaddress` in terminal 1
5. Run `python record_qr_vicon.py` from the `ros` folder in terminal 2
6. Slowly move the *Vicon-visual marker* in front of the camera (the python script will record an image every 3 seconds) making sure to cover the entire image frame and Vicon workspace visible from the camera
7. Press ESC when you collected enough (around 100 should suffice) images

#### Result
* `img_*.png` files created in the `data/qr_vicon_pics` folder
* Positions of the marker in the world reference frame (the Vicon frame) written to `config/qr_vicon_world_Npoints.yml`

### 2. Compute positions of the visual marker in the camera frame

#### Requirements
* Complete 1.
* OpenCV C++ library
* Camera calibration file `config/calibration_funstuffs_cam.yml` (https://docs.opencv.org/3.4/d4/d94/tutorial_camera_calibration.html); if the camera lens doesn't have a wide angle, not performing the camera calibration won't deteriorate too much the accuracy of the projection (especially if the points are not at the edges of the frame)

#### Steps
```
cd detect_and_store_qr
mkdir build
cd build
cmake ..
make
./detect_markers_images
```
The executable shows a window where the Aruco marker is highlighted in the image; you need to press a key to move forward with the images; in case there are still images where the Aruco marker is not detected, make a note of these images and delete them before repeating the process (i.e. before running `./detect_markers_images` again)

#### Result
* Positions of the marker in the image reference frame written to `config/qr_vicon_image_Npoints.yml`

## Test

#### Requirements
* Complete 1. & 2.
* Camera calibration file `config/calibration_funstuffs_cam.yml`

#### Steps
* `python main.py` (the code contains example config files, so you can actually try this out without performing 1. & 2.)

#### Results
* Transformation between world reference frame and image reference frame computed when the object of the `FunstuffsCam` class is created
* The world points are mapped to image points using the `project_point` method of the `FunstuffsCam` class
* Image with superimposed image points is displayed
