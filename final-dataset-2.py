""" final-exam_ROI.py
    USAGE: 
    
    $ python final-exam_ROI.py --video_file football-field-cropped-video.mp4 

    Code to detect an object inside an input video by varying the HSV values after converting the video to this format.

Authors:
+ Jenyfer Eugenia Toj López- jenyfer.toj@udem.edu
+ Julio Enrique Martinez Robledo- julio.martinezr@udem.edu
* Ian Luis Ramirez Mora - ian.ramirez@udem.edu


Institution: Universidad de Monterrey
Subject: Computational Vision
Lecturer: Dr. Andrés Hernández Gutiérrez

Date of creation: May 1st 2023
Last update: May 16th 2023
"""

# -----------------------  Import standard libraries ----------------------- #
from __future__ import print_function
import cv2 
import argparse
import numpy as np
import matplotlib.pyplot as plt
from time import strftime, gmtime

def get_pixel_coordinates(event, x, y, flags, param):
    """
        This function responds to an event of clicking to assign the coordinates
            :param event: type of event occurred with the mouse
            :param x: coordinate x of the pixel clicked
            :param y: coordinate y of the pixel clicked
            :param flags: flag to identify certain events with the mouse wheel
            :return: void
            """
    global coordinates
    global field_done
    # print(f"Current selected pixel (x,y): {x, y}")

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left button pressed. Pixel clicked (x,y): {x, y}")
        coord_list.append((x, y))
    elif flags == cv2.EVENT_FLAG_CTRLKEY:
        print("Field selected")
        field_done = 1

# ------------------ Define and initialize variables ---------------------- #
coord_list = list()
field_done = 0
co, ci, cd = 0, 0, 0
window_capture_name, window_output_name = 'Input video', 'Output video'

# ------------------ Parse data from the command line terminal ------------- #
parser = argparse.ArgumentParser(description='Vision-based object detection')
parser.add_argument('--video_file', type=str, default='camera', help='Video file used for the object detection process')
args = parser.parse_args()

# ------------------ Read video sequence file ------------------------------ #
cap = cv2.VideoCapture(args.video_file)

# Initialize the background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Define the minimum contour area for object detection
min_contour_area = 50

# ------------- Create two new windows for visualisation purposes ---------- #
cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_output_name)
cv2.setMouseCallback(window_capture_name, get_pixel_coordinates)

# ------------------------------ Main loop -------------------------------- #
while True:

    if co<1:
    # Read a frame from the video
        ret, frame = cap.read()

    # Check if the image was correctly captured
    if frame is None:
        break

    NPOINTS = len(coord_list)

    if field_done == 0:
        # Convert the list of coordinates to NumPy array
        points = np.array(coord_list, dtype=np.int32)
        # Reshape the points array to the required format for cv2.polylines()
        points = points.reshape((-1, 1, 2))
        # Draw the polygon on the image
        cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)

    else:
        ret, frame = cap.read()
        cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        mask_field = np.zeros(frame.shape, dtype=np.uint8)
        cv2.fillPoly(mask_field, [points], color=(0, 255, 0))
        bitwise_AND = cv2.bitwise_and(frame, mask_field)


    if field_done:
        frame_width = int(frame.shape[1])
        frame_height = int(frame.shape[0])

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(bitwise_AND)

        # Remove noise and perform thresholding
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, None)
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filter out small contours
            if cv2.contourArea(contour) > min_contour_area:
                # Draw bounding box around detected objects
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if (x+w/2 < (frame_width-80)/2):
                    ci+=1
                else:
                    cd+=1
        
    cv2.putText(img=frame, text = f"# Left {ci}, # Right: {cd}", org= (20,50), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.6, color = (0,0,0), thickness = 2) # Draw text above the rectangle for the time
    cv2.imshow(window_capture_name, frame) # Visualize both the input video and the object detection windows

    cd, ci = 0, 0

    co=co+1
    # The program finishes if the key 'q' is pressed
    key = cv2.waitKey(5)
    if key == ord('q') or key == 27:
        print("Programm finished, dude!")
        break
    
cv2.destroyAllWindows() # Destroy all visualisation windows
cap.release() # Destroy 'VideoCapture' object
