import cv2
import numpy as np
import os
import re

ix,iy = -1,-1
# mouse callback function for tracking mouse position on image
def mouse_pos(event,x,y,flags,param):
	global ix, iy			
	if event == cv2.EVENT_MOUSEMOVE:
		ix,iy = x,y
          
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

print_type = "Concentric Plane_slice_1"
print_run = "(1)"

dirIn = f"raw_data/{print_type}{print_run}"
processed = False

"""
labelsfile = open(dirIn + os.sep + f"labels{print_type}.csv","a")
labels=[]
for l in labelsfile:
     label = l.split(",")
     if len(labels)>0:
          if label[]
"""
     

csv = open(dirIn + os.sep + f"newlabels{print_type}.csv","a")

font = cv2.FONT_HERSHEY_SIMPLEX
image_num = 0
position_padding = 180
while(processed == False):
		


    #Sort files in numerical order
    dirFiles = os.listdir(dirIn)
    dirFiles.sort(key=natural_keys)
    
    if(processed == False):
        #Stream in directory of images
        for file in dirFiles:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                processed = True
                break

            img = cv2.imread(dirIn + os.sep + file,cv2.IMREAD_COLOR)
            cv2.rectangle(img,(250+position_padding,0+position_padding),(350+position_padding,100+position_padding),(255,0,0),3)
            cv2.rectangle(img,(250+position_padding,200+position_padding),(350+position_padding,300+position_padding),(0,255,0),3)
            cv2.rectangle(img,(150+position_padding,100+position_padding),(250+position_padding,200+position_padding),(0,0,255),3)
            cv2.rectangle(img,(350+position_padding,100+position_padding),(450+position_padding,200+position_padding),(0,0,255),3)
    
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',mouse_pos)
            cv2.imshow('image',img)

            if ix > 250+position_padding and ix < 350+position_padding and iy > 0+position_padding and iy <100+position_padding:
                 
                 csv.write(f"{file},z_high\n")
            elif ix > 250+position_padding and ix < 350+position_padding and iy > 200+position_padding and iy <300+position_padding:
                 
                 csv.write(f"{file},good\n")
            elif ix > 150+position_padding and ix < 250+position_padding and iy > 100+position_padding and iy <200+position_padding:
                 
                 csv.write(f"{file},e_low\n")
            elif ix > 350+position_padding and ix < 450+position_padding and iy > 100+position_padding and iy <200+position_padding:
                 
                 csv.write(f"{file},e_high\n")
            else:
                 
                 csv.write(f"{file},miss\n")

            cv2.waitKey(500)

            if(file == dirFiles[-2]):
                processed = True

            

            image_num += 1
		
cv2.destroyAllWindows()
csv.close()
