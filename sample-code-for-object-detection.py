""" stds-sample-code-for-object-detection.py
    USAGE: 
    
    $ python stds-sample-code-for-object-detection.py --video_file football-field-cropped-video.mp4 --frame_resize_percentage 100

    Code to detect an object inside an input video by varying the HSV values after converting the video to this format.

Authors:
+ Andres Hernandez Gutierrez - andres.hernandez@udem.edu
+ Julio Enrique Martinez Robledo- julio.martinezr@udem.edu

Institution: Universidad de Monterrey
Subject: Computational Vision
Lecturer: Dr. Andrés Hernández Gutiérrez

Date of creation: March 24th 2023
Last update: April 21st 2023
"""

# -----------------------  Import standard libraries ----------------------- #
from __future__ import print_function
import cv2 
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import strftime, gmtime

# ------------------------- Define utility functions ----------------------- #

def display_vision_analytic_metrics(image_width,image_height,x,y):

    '''
    Calculate the metrics of the chosen points using calculus and the focal
    length with the previous defined-in-class equations.
    All points are calculated with reference to the global plane.

            Args:
                    x (float): selected coordinate in pixels for the x-axis
                    y (float): selected coordinate in pixels for the y-axis
            Returns:
                    xg (float): analyzed metric coordinated in meters for 
                    the x-axis in reference to the global plane.
                    yg (float): analyzed metric coordinated in meters for 
                    the y-axis in reference to the global plane.
    '''
    zg = z-h_andres
    xg = ((x - image_width/2)/focal_length)*zg
    yg = ((y - image_height/2)/focal_length)*zg

    return xg,yg,zg

def calculate_distance(total_length,xg,yg):
    
    """
    Calculates the distance of a polygon by adding the lengths of each side.
    
            Args:
                total_length (float): The current total length.
                xg (list): A list of x-coordinates of the polygon vertices.
                yg (list): A list of y-coordinates of the polygon vertices.
    
            Returns:
                A tuple of the updated total length of the polygon perimeter and a list of the lengths of each side.
    """

    line_length_x, line_length_y = abs(xg[len(xg)-2] - xg[len(xg)-1]), abs(yg[len(yg)-2] - yg[len(yg)-1])
    length = np.sqrt(line_length_x**2+line_length_y**2)
    pace_list.append(length)
    total_length += length

    return total_length, pace_list

def update_3d_graph(text_box, total_length, xg_list, yg_list, zg_list):
    """
    Update a 3D graph with new data and update the text in a text box.

    Parameters:
    -----------
    text_box : matplotlib.text.Text
        The text box object to update with the new text.
    total_length : float
        The total length of the line in the graph.
    xg_list : list or array-like
        The x-coordinates of the points in the line.
    yg_list : list or array-like
        The y-coordinates of the points in the line.
    zg_list : list or array-like
        The z-coordinates of the points in the line.

    Returns:
    --------
    None
    """

    # Set the data for the line in the graph
    line3d.set_data(xg_list, yg_list)
    line3d.set_3d_properties(zg_list)

    # Format the total length and update the text box
    l = "{:.3f}".format(total_length)
    text_box.set_text(f"Accumulated Walking Distance: {l} m")


def update_pace_graph(frame_count_list, pace_list):
    """
    Update a 2D graph with new data.

    Parameters:
    -----------
    frame_count_list : list or array-like
        The x-coordinates of the points in the line.
    pace_list : list or array-like
        The y-coordinates of the points in the line.

    Returns:
    --------
    None
    """

    # Set the data for the line in the graph
    line2d.set_data(frame_count_list, pace_list)

    # Set the x-axis limit based on the last frame count value
    bx.set_xlim(0, frame_count_list[len(frame_count_list)-1])


# ------------------ Define and initialize variables ---------------------- #
h_andres, focal_length, total_distance, total_length, frame_number, z = 1.8, 1723.7245, 0, 0, 0, 50 # Value in meters for the height of the professor. # Value given in pixels for the problem.
max_value, max_value_H, low_H, low_S, low_V  = 255, 360//2, 90, 20, 0
high_H, high_S, high_V = max_value_H, max_value, max_value
window_capture_name, low_H_name, low_S_name, low_V_name, high_H_name, high_S_name, high_V_name = 'Input video', 'Low H', 'Low S', 'Low V', 'High H', 'High S', 'High V'
x_list, y_list, xg_list, yg_list, t_list, zg_list, length_list,frame_count_list, pace_list = list(),list(),list(),list(),list(),list(),list(),list(),list()
tracker = cv2.TrackerCSRT.create()

# ------------------ Parse data from the command line terminal ------------- #
parser = argparse.ArgumentParser(description='Vision-based object detection')
parser.add_argument('--video_file', type=str, default='camera', help='Video file used for the object detection process')
parser.add_argument('--frame_resize_percentage', type=float )
args = parser.parse_args()

# ------------------ Read video sequence file ------------------------------ #
cap = cv2.VideoCapture(args.video_file)

# ----------- Set the start and end frames through the frames -------------- #
start_time, end_time, frame_count, frame_rate = 18, 177, 0, cap.get(cv2.CAP_PROP_FPS) #0:18 in seconds, 2:57 in seconds
start_frame, end_frame = int(start_time * frame_rate), int(end_time * frame_rate)

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# ------------- Create two new windows for visualisation purposes ---------- #
cv2.namedWindow(window_capture_name)

# -------------------- Plot the data on the 3D plot ------------------------ #
fig = plt.figure("Localization")
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xg_list, yg_list, zg_list)

# Add labels and title
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('3D Localization of the Moving Object')
line3d, =  ax.plot(xg_list,yg_list,zg_list, "o-", color="blue")
text_box = ax.annotate('Initial Text', xy=(0.5, -0.15), xycoords='axes fraction',
                        xytext=(10, 10), textcoords='offset points',
                        ha='center', va='bottom', fontsize=7.5,
                        bbox=dict(facecolor='white', alpha=0.5))
ax.view_init(elev=-120,azim=-90)
ax.set_xlim(-54,54)
ax.set_ylim(-32,32)
ax.set_zlim(0,50)

# -------------------- Plot the data on the pace plot --------------------- #
fig2 = plt.figure("Pace")
bx = fig2.add_subplot()
line2d, =  bx.plot(frame_count_list,pace_list, "o-", color="green")
bx.set_ylabel('Pace (m)') # Set x-axis labels
bx.set_xlabel('Frame (Fps)') # Set y-axis labels
bx.set_title('Pace per 10fps') # Set title
bx.set_ylim(0,3)

# ------------------------------ Main loop -------------------------------- #
while True:

    # Read a frame from the video
    ret, frame = cap.read()

    # Check if the image was correctly captured
    if frame is None or cap.get(cv2.CAP_PROP_POS_FRAMES) > end_frame:
        break
        
    # Resize current frame
    width = int(frame.shape[1] * args.frame_resize_percentage / 100)
    height = int(frame.shape[0] * args.frame_resize_percentage / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    frame = cv2.medianBlur(frame,5) # Apply the median filter
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #Convert the current frame from BGR to HSV
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V)) # Apply a threshold to the HSV image
    framem = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the current frame from BGR to greyscale
    contours, _ = cv2.findContours(image=frame_threshold, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)  # Finding areas and contouring
    contours = sorted(contours, key=cv2.contourArea, reverse=True) # Sorting the contour based of area
    
    if contours:
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0]) # If any contours are found we take the biggest contour and get bounding box
        bbox = (x_min-15, y_min-15, box_width+15, box_height+15) # Select the region of interest
        t = frame_count/frame_rate

        if frame_count%10 == 0:
            x_list.append(x_min+box_width/2)
            y_list.append(y_min+box_height/2)

            xg, yg, zg = display_vision_analytic_metrics(width,height,x_list[len(x_list)-1],y_list[len(y_list)-1])
            xg_list.append(xg)
            yg_list.append(yg)
            zg_list.append(zg)

            if len(xg_list)>1:
                t_list.append(t)
                frame_count_list.append(frame_count)
                total_length, pace_list = calculate_distance(total_length,xg_list,yg_list)
                update_pace_graph(frame_count_list,pace_list)
                fig2.canvas.draw()

            # Update the plot
            update_3d_graph(text_box,total_length,xg_list,yg_list,zg_list)
            fig.canvas.draw()
            plt.pause(0.0001)
        
        if frame_number <= 35 or (6423 <= frame_number <= 6600):
            cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_min + box_width + 10, y_min + box_height + 10), (0, 255, 0), 2) # Draw rectangle according to HSV transformation
            cv2.putText(img=frame, text = "Person Detected", org= (x_min - 15, y_min - 15), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (0,255,0), thickness = 2) # Draw text above the rectangle
            tracker.init(frame_threshold, bbox) # Initialize the tracker with the ROI once we detect a full region of the object of interest
        else:
            success, bbox = tracker.update(frame_threshold) # Update the tracker with the current frame
            if success:
                x, y, w, h = [int(i) for i in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Drawing a rectangle around the object
                cv2.putText(img=frame, text = "Person Detected", org= (x - 15, y - 15), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (0,255,0), thickness = 2) # Draw text above the rectangle
                
    bitwise_AND = cv2.bitwise_and(frame, frame, mask=frame_threshold) # Filter out the grassy region from current frame and keep the moving object only
    tf = strftime("%H:%M:%S", gmtime(t+start_time))
    cv2.putText(img=frame, text = f"Time: {tf} s", org= (20,50), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (255,255,255), thickness = 3) # Draw text above the rectangle for the time
    cv2.imshow(window_capture_name, frame) # Visualize both the input video and the object detection windows

    # The program finishes if the key 'q' is pressed
    key = cv2.waitKey(5)
    if key == ord('q') or key == 27:
        print("Programm finished, dude!")
        break
    
    frame_count+=1

cv2.destroyAllWindows() # Destroy all visualisation windows
cap.release() # Destroy 'VideoCapture' object

# Plot the histogram of the frequency in the pace
plt.figure('Histogram')
plt.hist(pace_list, bins=30)
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')
plt.title('Distance travelled between consecutive frame')
plt.show() # Show the plot
