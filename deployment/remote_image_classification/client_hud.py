import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# importing libraries 
import cv2 
import numpy as np 
import socket
import datetime
import time
import json

UDP_IP = "10.0.2.79" # set it to destination IP.. RPi in this case
UDP_PORT = 12345

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(1.0)

class_names=["good","over","under"]
class_confidence=["","","",""]
detection_count = [0,0,0]


# font
font = cv2.FONT_HERSHEY_DUPLEX
# org
org = (100, 100)
# fontScale
fontScale = 0.75
# Line thickness of 2 px
thickness = 2
angle = 0

colours = {"good":(0,200,0),
            "over":(0,0,200),
           "under":(200,0,0),
           "HUD":(200, 0, 200)
}

length, width = 1280, 720
c_length = int(length/2)
c_width = int(width/2)
top_right = 250
top_left = 150
# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture('vid2_line.mp4') 

# Check if camera opened successfully 
if (cap.isOpened()== False): 
    print("Error opening video file") 

#fourcc = cv2.VideoWriter_fourcc(*'h264')
#out = cv2.VideoWriter('output2.mp4', fourcc, 20.0, (1280,720))

label=""
colour = (0,0,0)
frame_num = 0
fps = 0
# Read until video is completed 
start = time.time()
while(cap.isOpened()): 
      
# Capture frame-by-frame 
    ret, frame = cap.read() 
    if ret == True: 
    # Display the resulting frame 
        #cv2.imshow('Frame', frame)
        if frame_num%5==0:
            data = frame[370-300:370+300,700-300:700+300]
            data = cv2.resize(data,(140,140))
            data = data.reshape(-1)

            sock.sendto(data.tobytes(),(UDP_IP,UDP_PORT))

            resp, server = sock.recvfrom(512)
            resp = json.loads(resp.decode())
        #print(resp[10])


        
        
        #Centre view finder
        #top left
        frame = cv2.line(frame,(c_length-250,c_width-250), (c_length-250,c_width-200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-250,c_width-250), (c_length-200,c_width-250), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-305,c_width-305), (c_length-305,c_width-200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-305,c_width-305), (c_length-200,c_width-305), colours["HUD"],1)
        #top right
        frame = cv2.line(frame,(c_length+250,c_width-250), (c_length+250,c_width-200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+250,c_width-250), (c_length+200,c_width-250), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+305,c_width-305), (c_length+305,c_width-200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+305,c_width-305), (c_length+200,c_width-305), colours["HUD"],1)
        #bottom left
        frame = cv2.line(frame,(c_length-250,c_width+250), (c_length-250,c_width+200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-250,c_width+250), (c_length-200,c_width+250), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-305,c_width+305), (c_length-305,c_width+200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length-305,c_width+305), (c_length-200,c_width+305), colours["HUD"],1)
        #bottom right
        frame = cv2.line(frame,(c_length+250,c_width+250), (c_length+250,c_width+200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+250,c_width+250), (c_length+200,c_width+250), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+305,c_width+305), (c_length+305,c_width+200), colours["HUD"],1)
        frame = cv2.line(frame,(c_length+305,c_width+305), (c_length+200,c_width+305), colours["HUD"],1)

        #Border
        #left
        frame = cv2.line(frame,(10,10), (10,width-10), colours["HUD"],1)
        frame = cv2.line(frame,(10,10), (20,10), colours["HUD"],1)
        frame = cv2.line(frame,(10,width-10), (20,width-10), colours["HUD"],1)
        #right
        frame = cv2.line(frame,(length-10,10), (length-10,width-10), colours["HUD"],1)
        frame = cv2.line(frame,(length-10,10), (length-20,10), colours["HUD"],1)
        frame = cv2.line(frame,(length-10,width-10), (length-20,width-10), colours["HUD"],1)
        #top
        frame = cv2.ellipse(frame, (c_length,0), (int(length/2),75), 0, 0, 360, colours["HUD"], 1) 
        #bottom
        frame = cv2.ellipse(frame, (c_length,width), (int(length/2),75), 0, 0, 360, colours["HUD"], 1) 

        #Right side detail
        frame = cv2.line(frame,(length-200,top_right-30), (length-200,top_right-100), colours["HUD"],1)
        frame = cv2.line(frame,(length-200,top_right-100),( length-300,top_right-100),  colours["HUD"],1)
        frame = cv2.line(frame,(length-200,top_right+270), (length-200,top_right+340), colours["HUD"],1)
        frame = cv2.line(frame,(length-200,top_right+340),( length-300,top_right+340),  colours["HUD"],1)

        #Right side text
        cv2.putText(frame, f"Time : {datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}", (length-275,top_right), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"Frame : {frame_num}", (length-275,top_right+30), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"FPS : {fps:.1f}", (length-275,top_right+60), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"Extrusion Factor : +0%", (length-275,top_right+120), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, "Accumulative Error:", (length-275,top_right+150), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"- Over: {resp[7]}", (length-275,top_right+180), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"- Under: {resp[8]}", (length-275,top_right+210), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"- Total: {resp[9]}", (length-275,top_right+240), font, .5, colour, 1, cv2.LINE_AA)

        #Confidence bars
        cv2.putText(frame, "Classification Confidence", (50,top_left), font, .5, colour, 1, cv2.LINE_AA)
        cv2.putText(frame, f"good:{resp[1]}", (50,top_left+30), font, .5, colours["good"], 1, cv2.LINE_AA)
        cv2.putText(frame, resp[4], (150,top_left+30), font, .5, colours["good"], 1, cv2.LINE_AA)
        
        cv2.putText(frame, f"over:{resp[2]}", (50,top_left+60), font, .5, colours["over"], 1, cv2.LINE_AA)
        cv2.putText(frame, resp[5], (150,top_left+60), font, .5, colours["over"], 1, cv2.LINE_AA)
        
        cv2.putText(frame, f"under:{resp[3]}", (50,top_left+90), font, .5, colours["under"], 1, cv2.LINE_AA)
        cv2.putText(frame, resp[6], (150,top_left+90), font, .5, colours["under"], 1, cv2.LINE_AA)
        
        #Detection bars
        bar_len = 200 / (resp[10]+resp[11]+resp[12])
        good_len = int(bar_len * resp[10])
        over_len = int(bar_len * resp[11])
        under_len = int(bar_len * resp[12])
        cv2.putText(frame, "Classification Total Split", (50,top_left+150), font, .5, colour, 1, cv2.LINE_AA)
        frame = cv2.rectangle(frame,(50,top_left+180),(50+good_len,top_left+280), colours["good"],-1)
        frame = cv2.rectangle(frame,(50+good_len,top_left+180),(50+good_len+over_len,top_left+280), colours["over"],-1)
        frame = cv2.rectangle(frame,(50+good_len+over_len,top_left+180),(50+good_len+over_len+under_len,top_left+280), colours["under"],-1)

        #Detection Label
        cv2.putText(frame, "Current Classification", (50,top_left+340), font, .5, colour, 1, cv2.LINE_AA)
        if(resp[0]=="good"):
            cv2.putText(frame, resp[0], (80,top_left+395), font, 1, colours["good"], 1, cv2.LINE_AA)
        elif(resp[0]=="over"):
            cv2.putText(frame, resp[0], (80,top_left+395), font, 1, colours["over"], 1, cv2.LINE_AA)
        elif(resp[0]=="under"):
            cv2.putText(frame, resp[0], (80,top_left+395), font, 1, colours["under"], 1, cv2.LINE_AA)
        frame = cv2.rectangle(frame,(50,top_left+360),(200,top_left+415), colours["HUD"],1)
        frame = cv2.line(frame,(125,top_left+415), (125,top_left+465), colours["HUD"],1)
        frame = cv2.line(frame,(125,top_left+465), (c_length-250-25,top_left+465), colours["HUD"],1)
        frame = cv2.circle(frame,(c_length-250,c_width+250),25, colours["HUD"],1)

        cv2.imshow('Frame', frame) 
        #out.write(frame)
        frame_num += 1
        fps = frame_num / (time.time()-start)
    # Press Q on keyboard to exit 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
  
# Break the loop 
    else: 
        break
  
# When everything done, release 
# the video capture object 
cap.release() 
#out.release()
# Closes all the frames 
cv2.destroyAllWindows() 

