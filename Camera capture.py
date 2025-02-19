import numpy as np
import cv2
from PIL import Image
import requests

# 定义 inner frame
YSTART = 300
XSTART = 700


GREEN = np.array([0, 255, 0]) #定义颜色


cap = cv2.VideoCapture(0) #打开摄像头默认摄像头，有1.2个就改成1或者2

# 设置框架的长度和宽度
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义 VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# 创建 QR code detector
qr_detector = cv2.QRCodeDetector()

i = 1
while True:
    ret, frame = cap.read()#ret是布尔值，表示是否读取这一帧 cap.read 表示从摄像头读取这一帧

    if not ret:
        print("无法获取视频帧")
        break

    # 提取内部框架并且绘制绿色边框
    inner = frame[YSTART:YSTART+448, XSTART:XSTART+448].copy()
    frame[YSTART-2:YSTART+448+2, XSTART-2:XSTART+448+2] = GREEN
    frame[YSTART:YSTART+448, XSTART:XSTART+448] = inner


    out.write(frame)

    # 检测二维码
    value, pts, _ = qr_detector.detectAndDecode(frame)

    if value:
        print(f"detect this qrcode: {value}")#打印二维码的内容

        # 使用二维码内容作为标识符，构造 URL 并发起 GET 请求
        identifier = value.strip()
        url = f"https://mad-shop.onrender.com/api/pickups/{identifier}?populate=items"
        response = requests.get(url)

        if response.status_code == 200:
            print("API is rise:", response.json())  # Print API response JSON data
        else:
            print(f"can't get data。HTTP 状态码: {response.status_code}")

    # display frame
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF  #等待一秒钟
    if key == ord('q'):
        break
    elif key == ord('w'):
        # change bgr to rgb   bgr is also uesd in opencv
        a = inner[:,:,0].copy()
        b = inner[:,:,1].copy()
        c = inner[:,:,2].copy()
        inner[:,:,0] = c
        inner[:,:,1] = b
        inner[:,:,2] = a

        im = Image.fromarray(inner) #write image
        im = im.resize((224, 224))
        im.save(f'out{i:04d}.png')
        i += 1

# Release
cap.release()
out.release()
cv2.destroyAllWindows()