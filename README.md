# Image Similarity using pixel and hue values

This program can be used to find two most similar images by comparing their pixel and histogram euclidean values. It provides the difference rates for each images within a group and these values can be used to identify similar images.

## Objective

During my intern in KAIST CDSN Lab, I tested if Raspberry Pi can be used to identify the same person by comparing images taken from two different locations.
Utilizing Tensorflow for developing person-reidenfication was highly effective (83.6% accuracy), but sending images constantly to the Edge Server for computational result had a bottleneck effect, slowing IoT devices to track individuals in real-time. 

Since Raspberry Pi isn't powerful enough to run ML algorithm, I tested if pixel and hue values would be enough to track a person from two different locations. However, since human images were extracted by using YOLO program (software to identify objects) https://pjreddie.com/darknet/yolo/, each images had different width and height, giving significantly different pixel and hue values for comparison. 

## Further Consideration

Taking a human photos with YOLO for pixel/hue comparison isn't sufficient for tracking individuals since each images have too much significant pixel and hue differences. In order to increase its accuracy from 83.6% to above 90% using ML, utilizing Tensorflow to detect other characteristics such as clothings, color, etc will help significantly. Also, having a software to correct panorama distortion would greatly increase the accuracy of the program.
