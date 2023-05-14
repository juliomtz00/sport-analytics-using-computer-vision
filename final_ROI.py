""" stds-sample-code-for-object-detection.py


    USAGE:
    $ python stds-sample-code-for-object-detection.py --video_file football-field-cropped-video.mp4 --frame_resize_percentage 30

"""

# -----------------------  Import standard libraries ----------------------- #
from __future__ import print_function
import cv2
import argparse
import numpy as np


# Initialize list
coord_list = list()
field_done = 0
# Get image coordinates
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

def compute_line_segments(NPOINTS):
    """
        This function implements the computation of each line segment and inserts a circle on the clicked coordinate and
        visualize them on every frame retrieved by the webcam
            :param NPOINTS: coordinate list length
            :return: void
            """
    # loop through the coordinate of each clicked pixel
    for coordinate, icoord in zip(coord_list, range(NPOINTS)):

        if icoord >= 1:
            cv2.line(img=frame, pt1=temp_coordinate, pt2=coordinate, color=(0, 0, 0), thickness=2)

        # Drae a circle on the current line
        cv2.circle(img=frame, center=coordinate, radius=4, color=(0, 0, 255), thickness=-1)
        temp_coordinate = coordinate

# ------------------ Define and initialise variables ---------------------- #
max_value = 255
max_value_H = 360 // 2
window_capture_name = 'Input video'
window_detection_name = 'Object Detection'

# ------------------ Parse data from the command line terminal ------------- #
parser = argparse.ArgumentParser(description='Vision-based object detection')
parser.add_argument('--video_file', type=str, default='camera', help='Video file used for the object detection process')
args = parser.parse_args()

# ------------------ Read video sequence file ------------------------------ #
cap = cv2.VideoCapture(args.video_file)

fps = cap.get(cv2.CAP_PROP_FPS)
minuto_inicial = 0
posicion_inicial = int(minuto_inicial * 60 * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, posicion_inicial)

# ------------- Create two new windows for visualisation purposes ---------- #
cv2.namedWindow(window_capture_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_detection_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_capture_name, get_pixel_coordinates)

# ------- Main loop --------------- #
while True:

    # Read current frame
    ret, frame = cap.read()

    # Check if the image was correctly captured
    if frame is None:
        break

    NPOINTS = len(coord_list)
    # compute_line_segments(NPOINTS)
    print(frame.shape)
    if field_done == 0:
        # Convert the list of coordinates to NumPy array
        points = np.array(coord_list, dtype=np.int32)
        # Reshape the points array to the required format for cv2.polylines()
        points = points.reshape((-1, 1, 2))
        # Draw the polygon on the image
        cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)
    else:
        cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        mask_field = np.zeros(frame.shape, dtype=np.uint8)
        cv2.fillPoly(mask_field, [points], color=(0, 255, 0))
        bitwise_AND3 = cv2.bitwise_and(frame_HSV, mask_field)

    # Convert the current frame from BGR to HSV
    frame_HLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # Apply a threshold to the HSV image
    frame_threshold = cv2.inRange(frame_HLS, (0, 0, 81), (180, 255, 255))
    frame_threshold[0:70,:]=0
    frame_threshold[670:-1, :] = 0
    # Filter out the grassy region from current frame and keep the moving object only

    bitwise_AND = cv2.bitwise_and(frame, frame, mask=frame_threshold)

    frame_HSV = cv2.cvtColor(bitwise_AND, cv2.COLOR_BGR2HSV)

    #frame_HSV = cv2.medianBlur(frame_HSV, 3)
    # Apply a threshold to the HSV image
    frame_threshold2 = cv2.inRange(frame_HSV, (40, 0, 0), (180, 255, 255))


    # Filter out the grassy region from current frame and keep the moving object only
    bitwise_AND2 = cv2.bitwise_and(frame, bitwise_AND, mask=frame_threshold2)

    # Visualise both the input video and the object detection windows
    cv2.imshow(window_capture_name, frame)
    if field_done:
        cv2.imshow(window_detection_name, bitwise_AND3)
    else:
        cv2.imshow(window_detection_name, frame_HSV)

    # The program finishes if the key 'q' is pressed
    key = cv2.waitKey(5)
    if key == ord('q') or key == 27:
        print("Programm finished, mate!")
        break

# Destroy all visualisation windows
cv2.destroyAllWindows()

# Destroy 'VideoCapture' object
cap.release()