import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import socket
import cv2
import io
import numpy as np
import time
import json

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 12345 # port

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
model_path = "/Users/daniel/Documents/aiPrint-Publishable/aiPrint-Data-Creation/cnn-training/results-"
models ={"1" : tf.keras.models.load_model(f'{model_path}transfer/MobileNetV3Small_infill.h5'),
         "2" : tf.keras.models.load_model(f'{model_path}transfer/MobileNetV3Small_line.h5'),
         "3" : tf.keras.models.load_model(f'{model_path}real/ResNet50V2_infill.h5'),
         "4" : tf.keras.models.load_model(f'{model_path}real/ResNet50V2_line.h5'),
         "5" : tf.keras.models.load_model(f'{model_path}transfer/ResNet50V2_infill.h5'),
         "6" : tf.keras.models.load_model(f'{model_path}transfer/ResNet50V2_line.h5'),
         "7" : tf.keras.models.load_model(f'{model_path}real/Xception_infill.h5'),
         "8" : tf.keras.models.load_model(f'{model_path}real/Xception_line.h5'),
         "9" : tf.keras.models.load_model(f'{model_path}transfer/Xception_infill.h5'),
         "10" : tf.keras.models.load_model(f'{model_path}transfer/Xception_line.h5')}
class_names=["good","over","under"]
class_confidence=["","","",""]
detection_count = [0,0,0]
label = ""
run_counter = 30
while True:
    data, addr = sock.recvfrom(999999) # random buffer size, doesn't matter here..

    image = np.frombuffer(data, np.uint8)
    image = image.reshape(140,140,3)
    image = cv2.resize(image,(224,224))
    cv2.imwrite("test.png", image)
    input_data = np.expand_dims(image, axis=0)
    details=""
    votes = []
    scores = []
    run_counter +=1
    if run_counter <= 5:
        model = "1"
    elif run_counter <=10:
        model = "2"
    elif run_counter <=15:
        model = "3"
    elif run_counter <=20:
        model = "4"
    elif run_counter <=25:
        model = "5"
    elif run_counter <=30:
        model = "6"
    elif run_counter <=35:
        model = "7"
    elif run_counter <=40:
        model = "8"
    elif run_counter <=45:
        model = "9"
    elif run_counter <=50:
        model = "10"
    start = time.time()
    predictions = models[model].predict(input_data, verbose = 0)
    stop = time.time()
    score = tf.nn.softmax(predictions[0])
    votes.append([class_names[np.argmax(score)], score[np.argmax(score)]])
    scores.append(predictions[0])
    details += f"{model} good {predictions[0][0]:.5f} over {predictions[0][1]:.5f} under {predictions[0][2]:.5f}\n"

    winner = 0
    #Worst case classification
    if scores[winner][0] < 0.9:
        c = np.argmax([scores[winner][1],scores[winner][2]])+1
        label = class_names[c]
        detection_count[c] +=1
    else:
        label = "good"
        detection_count[0] +=1

    
    #Confidence bars
    for idx, s in enumerate(scores[winner]):
        bar = ""
        for i in range(int(float(s)*30)):
            bar+="|"
        class_confidence[idx]=bar
    cv2.imwrite("result.jpg", image)
    
    packet = [label, f"{scores[winner][0]:.3f}",f"{scores[winner][1]:.3f}", f"{scores[winner][2]:.3f}",class_confidence[0],class_confidence[1],class_confidence[2],
              f"{(100 / sum(detection_count)) * (detection_count[1]):.2f}%",
              f"{(100 / sum(detection_count)) * (detection_count[2]):.2f}%",
              f"{(100 / sum(detection_count)) * (detection_count[0]):.2f}%",
              detection_count[0],
              detection_count[1],
              detection_count[2],
              stop-start]
   
    sock.sendto(bytes(json.dumps(packet), 'utf-8'), addr)
