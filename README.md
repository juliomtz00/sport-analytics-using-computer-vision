# sports-analytics-using-computer-vision

## Introduction to vision analytics and 3D localization of moving objects
Both vision analytics and 3D localization of moving objects use computer vision techniques to precisely estimate the position and motion of things in three-dimensional space. These two topics are closely related. Vision analytics, sometimes referred to as computer vision analytics, is the practice of applying computer vision algorithms to analyze and extract useful insights from visual data, such as photos or videos. 
To evaluate the substance of visual data and extract useful information from it, algorithms and models must be applied. Vision analytics can be applied to the tracking and identification of moving objects, the detection of events or abnormalities, the measurement of object attributes, and several other analyses. Typical tasks include behavior analysis, object tracking, activity recognition, and object detection. Accurately determining an object’s position and motion in a three-dimensional space is referred to as the 3D localization of moving objects. It entails using information gleaned from visual input to recreate the geographical coordinates of real-world objects. Computer vision techniques use a variety of methods, including stereo vision, depth estimation, motion analysis, and sensor fusion, to accomplish 3D localization. 
In order to infer depth information and recreate the 3D world, stereo vision depends on the discrepancy between many cameras. Utilizing a single camera, depth estimation techniques can also be used by examining the size, shape, and other visual characteristics of objects. It is feasible to comprehend an item’s position, trajectory, speed, and other important characteristics by precisely localizing the object in 3D space. Numerous applications, such as augmented reality, robotics, object tracking, navigational systems, and immersive experiences, depend on this information. 
Exciting new possibilities for the real-time comprehension and analysis of dynamic scenes are made possible by the combination of vision analytics and 3D localization of moving objects. It makes it possible for robots to observe and comprehend the visual world, enabling more intelligent and human-like automation, decision-making, and environmental interaction.

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/applications.png"/>

## Problem statement
Provided a couple of video sequences captured by an aerial vehicle that was hovering on one of UDEM’s soccer fields.2.
For dataset 1, your proposed algorithm must:
• Detect the moving soccer ball throughout the video sequence.
• Count the number of times the ball visits the left and right sides of the soccer field enclosed by the green region. This information should be visualized on the current frame - choose a proper location.

For dataset 2, your proposed algorithm must:
• Detect the moving soccer players throughout the video sequence.
• Detect the moving soccer ball throughout the video sequence. The detected soccer ball has been enclosed in a color different from that used to represent the seen players; feel free to use either the same or different colors.
• Count the number of players on each side of the soccer field throughout the complete sequence. This information should be visualized on the current frame - choose a location.

## Materials
• A personal computer.
• 1280x720 Video sequence 1 (177.8MB).
• 1280x720 Video sequence 2 (186.4 MB).
• Internet connectivity, as you may need to install Python libraries.
• Python 3.10 using the following libraries: OpenCV, NumPy, ArgParse, glob, and text-wrap.
• Optionally: PyCharm, IDE, Visual Studio Code, Sublime, Atom, Gedit, etc.

## Metodology
First and foremost, the requirements of the problem must be analyzed. For dataset 1, the algorithm must detect a moving soccer ball that’s moving throughout the video sequence, while also counting the number of times that the ball visits the left and right sides of the soccer field enclosed by the green region that encompasses the grass inside the soccer field. On the other hand, for dataset 2, the deliverable must detect the moving soccer players throughout the video sequence, while also detecting the moving soccer ball throughout the video sequence. Finally, the number of players on each side of the soccer field throughout the complete sequence must be counted and visualized on the current frame. As two different video datasets must be processed, where the video deliverables are virtually different from each other and have different requirements, it must be assumed that two coding files must be made, considering the time that we have to develop the scripts.

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/frame-hls.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/frame-hsv.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/frame-hls-min.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/field-1.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/field-2.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/perimeter.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/perimeter-min.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/count.png"/>

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/count-min.png"/>

In detail, the description of each step to filter the image in the program for the first video is shown:
• We started off by making a color space transformation so we could filter out the grass of the field, we obtained an image like the one shown in the figure 5.
• After we checked for a combination of H-L-S elements that would filter out the grass. We ended up assigning the following values to Low/High HLS: frame threshold = cv2.inRange(frame- HLS, (0, 0, 81), (180, 255, 255)) and obtaining an image like the one shown in the figure 6.
• After we applied a bitwise between these 2 first images we did an HSV color space transformation to get a better glance at the ball, as seen in the figure 7.
• Subsequently, a second threshold was generated to remove and recognize even more important points that will help us in the solution of the problem. This was done through the usage of the following function: cv2.inRange(frame-HSV, (40, 0, 0), (180, 255, 255)). As seen in figure 8.
• A third threshold was done, this time by subtracting the obtained points from the first image from the points from the second one, as main lines were seen in the second one and if they are subtracted, they can be deleted from the image 9.
• In pair with the threshold, the combination with the bitwise-AND function (cv2.bitwiseand(bitwise-AND, bitwise-AND, mask=frame-threshold3)) to filter was applied, obtaining more clean images with only a few lines shown. This is done mainly to filter out the grassy region from the current frame and keep the moving object only. 10 11.
• At the end, we applied a Gaussian blur to use the OpenCV function to detect edges cv2.Canny; as there was some noise at the field provoked by a painted line as seen in figure 12 we applied a Hough transform to detect mentioned line and check if the circle coordinates were within its limits so the algorithm will omit those and detect only the ball, Additionally we added an extra Gaussian blur within the limits of the detected line, to reduce the noise caused by that line. The results can be observed in figure 13. Nevertheless we still have noise in the football field because of lightning variations and occlusion, for example, in certain frames heads of the football players are detected as the ball.

For the second script, the following steps were done, as a new method was intended to see which one worked better in filtering the players walking inside the field:
• More research was done and instead of fully manually filtering as we did in the previous script, the function cv2.createBackgroundSubtractorMOG2() was selected to use this function for background subtractor and get a better tracking of the movement.
• The function to apply morphology is established to remove noise.
• Then, the threshold is performed, developing a good filtering as seen.
• Finally, the usual function to detect corners is applied for every found point inside the image, and rectangles are drawn in these coordinates.

As an additional comment, a function was added to both scripts to establish the perimeter of the soccer field and it was specified to stop the frame at the beginning until the user has defined the perimeter correctly which is completed when they click on the CTRL key while moving the mouse or trackpad.

## Results
As a result, we were able to comply with the requirements and problem, by filtering the image and showing the number of times that the ball was on each side, even though because of a mistake in recognizing only the ball, as it still isn’t fully filtered, some points are being taken into account even though they don’t correspond to the ball moving as seen in figure 15. It can be seen in Figure 16 that the count is being done, even though it is not dynamic as we would have wanted and was discussed in class, as it wasn’t able to be done within the given time, but the problem statement is mainly resolved, taking some minor processing errors into consideration.

<img src="https://github.com/juliomtz00/final-exam-vision-udem/blob/7111cc6333c715a314cc960c0bb406f3124b1192/images/results1.png"/>
