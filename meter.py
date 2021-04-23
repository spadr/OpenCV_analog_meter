import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def getXY(r, degree):
    rad = math.radians(degree)
    x = r * math.cos(rad)
    y = r * math.sin(rad)
    return int(x), int(y)

img = cv2.imread('sample.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 100)

circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,100,20,param1=30,param2=30,minRadius=300,maxRadius=700)

shape = img.shape

circles = np.uint16(np.around(circles))
i = circles[0,0]
if (shape[0]//4 <= i[0]) and (i[0] <= shape[0]*3//4) and (shape[1]//4 <= i[1]) and (i[1] <= shape[1]*3//4):
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

cv2.imwrite("output.jpg",img)
process_data = gray

resized_img = []

for n in range(int(i[2]/1.414)):
    j = n + 2
    #直交座標を使ってますが、極座標を使う方法もあると思います
    up    = process_data[ i[1]-j          , i[0]-j : i[0]+j ]
    down  = process_data[ i[1]+j          , i[0]-j : i[0]+j ]
    left  = process_data[ i[1]-j : i[1]+j ,           i[0]-j]
    right = process_data[ i[1]-j : i[1]+j ,           i[0]+j]
    left  = left[1:-1]
    right = right[1:-1]
    #print(up.shape, down.shape, left.shape, right.shape)
    resize_up    = cv2.resize(up    , (1 , i[2]    )).flatten()
    resize_down  = cv2.resize(down  , (1 , i[2]    )).flatten()
    resize_left  = cv2.resize(left  , (1 , i[2] -2 )).flatten()
    resize_right = cv2.resize(right , (1 , i[2] -2 )).flatten()
    #print(resize_up.shape, resize_down.shape, resize_left.shape, resize_right.shape)
    line = resize_down[ : i[2]//2][::-1]
    line = np.append(line, resize_left[::-1])
    line = np.append(line, resize_up)
    line = np.append(line, resize_right)
    line = np.append(line, resize_down[i[2]//2 : ][::-1])
    print(line)
    print(line.shape)
    resized_img.append(line)


resized_img = np.array(resized_img ,dtype='uint8')
cv2.imwrite("output2.jpg",resized_img)

resized_img = np.array(resized_img ,dtype="int64")
pin = np.sum(resized_img , axis=0)
plt.plot(pin)
plt.show()

degree = 360 * (np.argmin(pin)/len(pin))
print("degree:",degree)

x,y = getXY(i[2]/1.414,degree-90)

img = cv2.line(img,(i[0],i[1]),(i[0]-x,i[1]-y),(255,0,0),5)
cv2.imwrite("output3.jpg",img)