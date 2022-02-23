#!/usr/bin/env python
from include.FunstuffsCam import FunstuffsCam
import numpy as np
import cv2

fc = FunstuffsCam()

img = cv2.imread("data/test_image.png")

# create some world points: 10 circles of radii ranging from 1m and 0.1m, and of height equal to 1-radius
Npoints = 50
for r in np.linspace(0.1, 1, num=10):
    X = r * np.cos(np.linspace(0, 2*np.pi, Npoints))
    Y = r * np.sin(np.linspace(0, 2*np.pi, Npoints))
    Z = (1-r) * np.ones((Npoints))
    for n in range(Npoints):
				# project each point to the image frame
        im_pt = fc.project_point(np.array([(X[n], Y[n], Z[n])]))
				# plot each point as a red filled circle
        cv2.circle(img, (int(im_pt[0]), int(im_pt[1])), 8, (0,0,255), -1)

# plot the origin of the world reference frame
origin = fc.project_point(np.array([(0.0,0.0,0.0)]))
cv2.circle(img, (int(origin[0]), int(origin[1])), 16, (0,255,0), -1)

# show the image
# img = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
cv2.imshow("img", img)
while cv2.waitKey() != 27:
    pass
