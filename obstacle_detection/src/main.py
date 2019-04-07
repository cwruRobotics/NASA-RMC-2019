#!/usr/bin/env python
import os
import sys
import numpy as np
import cv2
import time
import math
import pandas as pd
from obstacle_detection import get_obstacles_with_plane
from depth_image_processing import *
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

try:
    from pylibfreenect2 import OpenCLPacketPipeline

    pipeline = OpenCLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenGLPacketPipeline

        pipeline = OpenGLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline

        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)

# Create and set logger
logger = createConsoleLogger(LoggerLevel.Debug)
setGlobalLogger(logger)

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

device.start()

# NOTE: must be called after device.start()
registration = Registration(device.getIrCameraParams(),
                            device.getColorCameraParams())

h, w = 512, 424
FOVX = 1.232202  # horizontal FOV in radians
focal_x = device.getIrCameraParams().fx  # focal length x
focal_y = device.getIrCameraParams().fy  # focal length y
principal_x = device.getIrCameraParams().cx  # principal point x
principal_y = device.getIrCameraParams().cy  # principal point y
undistorted = Frame(h, w, 4)
registered = Frame(h, w, 4)

thetas = np.array([])
phis = np.array([])
obstacle_list = []
obstacle_id = 0

visualize = False
save_frames = True

print(os.getcwd())

while True:
    frames = listener.waitForNewFrame()
    depth_frame = frames["depth"]
    color = frames["color"]
    registration.apply(color, depth_frame, undistorted, registered)
    img = depth_frame.asarray(np.float32) / 4500.
    color_frame = registered.asarray(np.uint8)
        
    output = get_obstacles_with_plane(img,
                                      color_frame,
                                      obstacle_list,
                                      thetas,
                                      phis,
                                      obstacle_id,
                                      send_data=True,
                                      visualize=visualize,
                                      save_frames=save_frames)
    
    if visualize:
        key = cv2.waitKey(delay=1)
        if key == ord('q'):
            break
    listener.release(frames)

device.stop()
device.close()

sys.exit(0)
