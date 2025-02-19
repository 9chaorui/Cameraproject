import numpy as np
import cv2
from PIL import Image
import requests

YSTART = 300
XSTART = 700

GREEN = np.array([0, 255, 0]) 

cap = cv2.VideoCapture(0) 

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

qr_detector = cv2.QRCodeDetector()

i = 1
while True:
    ret, frame = cap.read()

    if not ret:
        print("can not get frame")
        break
    
    inner = frame[YSTART:YSTART+448, XSTART:XSTART+448].copy()
    frame[YSTART-2:YSTART+448+2, XSTART-2:XSTART+448+2] = GREEN
    frame[YSTART:YSTART+448, XSTART:XSTART+448] = inner


    out.write(frame)
    
    value, pts, _ = qr_detector.detectAndDecode(frame)

    if value:
        print(f"detect this qrcode: {value}")
    
        identifier = value.strip()
        url = f"https://mad-shop.onrender.com/api/pickups/{identifier}?populate=items"
        response = requests.get(url)

        if response.status_code == 200:
            print("API is rise:", response.json())  
        else:
            print(f"can't get data.HTTP : {response.status_code}")
    
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF  
    if key == ord('q'):
        break
    elif key == ord('w'):
        
        a = inner[:,:,0].copy()
        b = inner[:,:,1].copy()
        c = inner[:,:,2].copy()
        inner[:,:,0] = c
        inner[:,:,1] = b
        inner[:,:,2] = a

        im = Image.fromarray(inner) 
        im = im.resize((224, 224))
        im.save(f'out{i:04d}.png')
        i += 1

cap.release()
out.release()
cv2.destroyAllWindows()

#I install opencv and image and requests for my code to capture video,image and for http 
#i create videowriter to make the style of video is mp4 and make qrdetector to detect qr code . this depends opencv's qr scan
#also i create 2 buttons is key=q and key=w   q is quit the terminal and w to save frame.
#for the third question, i don't understand very well , but the first one and the second question i can get from my code .and i do some try for the third one.
