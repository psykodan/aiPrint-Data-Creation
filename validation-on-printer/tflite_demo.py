import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# importing libraries 
import cv2 
import numpy as np 
import tensorflow as tf
import pathlib
import sys

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="/Users/daniel/Documents/aiPrint-Publishable/aiPrint-Data-Creation/deployment/optimised_models/MobileTransfer_line.tflite")
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# input details
print(input_details)
# output details
print(output_details)
interpreter.allocate_tensors()

class_names=["good","over","under"]
class_confidence=["","","",""]
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (100, 100)
# fontScale
fontScale = 0.75
# Blue color in BGR
color = (255, 0, 0)

colours = [(0,255,0),#perfect
            (150,150,255),#over
           (255,150,150)#under
]
# Line thickness of 2 px
thickness = 2
angle = 0

x, y, width, height = 800, 320, 300, 300

# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture('vid2_line.mp4') 
  
# Check if camera opened successfully 
if (cap.isOpened()== False): 
    print("Error opening video file") 


frame_num = 0
# Read until video is completed 
while(cap.isOpened()): 
      
# Capture frame-by-frame 
    ret, frame = cap.read() 
    if ret == True: 
    # Display the resulting frame 
        #cv2.imshow('Frame', frame) 
        cropped_frame = frame[y-height:y+height, x-width:x+width]
        resized_frame = cv2.resize(cropped_frame,(224,224))
        resized_frame = np.float32(resized_frame)
        interpreter.set_tensor(input_details[0]['index'], [resized_frame])
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        score = tf.nn.softmax(output_data[0])
        str_label = class_names[np.argmax(score)]

        print(str_label)
    

        cv2.imshow('Frame', frame) 
        frame_num += 1
    # Press Q on keyboard to exit 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
  
# Break the loop 
    else: 
        break
  
# When everything done, release 
# the video capture object 
cap.release() 
  
# Closes all the frames 
cv2.destroyAllWindows() 
