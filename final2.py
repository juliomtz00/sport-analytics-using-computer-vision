""" stds-sample-code-for-object-detection.py


    USAGE:
    $ python stds-sample-code-for-object-detection.py --video_file football-field-cropped-video.mp4 --frame_resize_percentage 30

"""

# -----------------------  Import standard libraries ----------------------- #
from __future__ import print_function
import cv2
import argparse
import numpy as np

# ------------------------- Define utility functions ----------------------- #
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)


# ------------------ Define and initialise variables ---------------------- #
max_value = 255
max_value_H = 360 // 2
low_H = 1
low_S = 0
low_V = 0
high_H = 19
high_S = 255
high_V = 255
window_capture_name = 'Input video'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

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
cv2.namedWindow("test", cv2.WINDOW_NORMAL)

# ------------ Configure trackbars for the low and hight HSV values -------- #
cv2.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

# ------- Main loop --------------- #
while True:

    # Read current frame
    ret, frame = cap.read()

    # Check if the image was correctly captured
    if frame is None:
        break

    # Resize current frame

    print(frame.shape)
    # Apply the median filter
    #

    # Convert the current frame from BGR to HSV
    frame_HLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # Apply a threshold to the HSV image
    frame_threshold = cv2.inRange(frame_HLS, (0, 0, 81), (180, 255, 255))
    frame_threshold[0:70,:]=0
    frame_threshold[670:-1, :] = 0
    frame_threshold = cv2.medianBlur(frame_threshold, 3)
    # Filter out the grassy region from current frame and keep the moving object only
    bitwise_AND = cv2.bitwise_and(frame, frame, mask=frame_threshold)

    frame_HSV = cv2.cvtColor(bitwise_AND, cv2.COLOR_BGR2HSV)

    #frame_HSV = cv2.medianBlur(frame_HSV, 3)
    # Apply a threshold to the HSV image
    frame_threshold2 = cv2.inRange(frame_HSV, (36, 0, 0), (180, 255, 255))
    frame_threshold3 = frame_threshold-frame_threshold2
    #frame_threshold3 = cv2.medianBlur(frame_threshold3, 3)
    bitwise_AND3 = cv2.bitwise_and(bitwise_AND, bitwise_AND, mask=frame_threshold3)
    frame_HLS2 = cv2.cvtColor(bitwise_AND3, cv2.COLOR_BGR2HLS)
    frame_threshold4 = cv2.inRange(frame_HLS2, (low_H, low_S, low_V), (high_H, high_S, high_V))
    #frame_threshold4 = cv2.medianBlur(frame_threshold4, 3)
    bitwise_AND3 = cv2.bitwise_and(bitwise_AND, bitwise_AND, mask=frame_threshold4)


    bitwise_AND3=cv2.cvtColor(bitwise_AND3, cv2.COLOR_RGB2GRAY)

    # Detección de bordes con Canny
    # Aplicar un filtro Gaussiano para reducir el ruido
    #bitwise_AND3 = cv2.GaussianBlur(bitwise_AND3, (5, 5), 0)
    # Detección de bordes con Canny
    edges = cv2.Canny(bitwise_AND3, 15, 50)
    if(np.count_nonzero(sum(edges))>0):
        # Detectar los círculos en la imagen
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=1, minRadius=5, maxRadius=10)

        #print(circles)
        # Convertir las coordenadas y los radios a enteros
        circles = np.uint16(np.around(circles))
        # Dibujar los círculos encontrados en la imagen original
        for i in circles[0, :]:
            # Dibujar el círculo exterior
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Dibujar el centro del círculo
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
        # Filter out the grassy region from current frame and keep the moving object only


    # Visualise both the input video and the object detection windows
    cv2.imshow(window_capture_name, frame_HLS2)
    cv2.imshow(window_detection_name, bitwise_AND3)
    cv2.imshow("test", frame)
    # The program finishes if the key 'q' is pressed
    key = cv2.waitKey(5)
    if key == ord('q') or key == 27:
        print("Programm finished, mate!")
        break

# Destroy all visualisation windows
cv2.destroyAllWindows()

# Destroy 'VideoCapture' object
cap.release()