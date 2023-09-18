# final-exam-vision-udem

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
