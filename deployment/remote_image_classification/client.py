import socket
import io
import time
import time, libcamera
from picamera2 import Picamera2, Preview
import cv2

picam = Picamera2()

#config = picam.create_preview_configuration(main={"size": (224, 224)})
config = picam.create_still_configuration(main={"size":(640,480)})
picam.configure(config)
picam.start()

UDP_IP = "10.0.2.79" # set it to destination IP.. RPi in this case
UDP_PORT = 12345

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(1.0)


cap = cv2.VideoCapture('vid2_line.mp4')

while(cap.isOpened()):
    ret, data = cap.read()
    if ret == True:
        #data = picam.capture_array()
        #data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        data = data[370-300:370+300,700-300:700+300]
        data = cv2.resize(data,(140,140))
        data = data.reshape(-1)

        sock.sendto(data.tobytes(),(UDP_IP,UDP_PORT))

        resp, server = sock.recvfrom(512)
        print(resp.decode())

        #time.sleep(0.05)
        
cap.release()
