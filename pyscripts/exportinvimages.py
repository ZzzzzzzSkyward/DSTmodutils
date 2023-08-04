'''
批量导出物品栏64x64大小图片
'''
import cv2
def imread(path,flags=-1):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)
    
def imwrite(path,img):
    return cv2.imencode('.png', img)[1].tofile(path)

import os
import re
import sys
import numpy as np
maxsize=64
color=[0,0,0,0]
def get_image():
    a=[i for i in  os.listdir(src) if i.endswith("png")]
    return a
def process(path):
    img = imread(path, cv2.IMREAD_UNCHANGED)
    height, width, channels = img.shape
    # 查找非零像素的坐标
    a=cv2.split(img)[3]
    box = cv2.findNonZero(a)
    x, y, w, h = cv2.boundingRect(box)
    img = img[y:y+h, x:x+w]
    height, width, channels = img.shape
    
    new_size = max(height, width)
    delta_w = new_size - width
    delta_h = new_size - height
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    
    img2 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    img2 = cv2.resize(img2, (maxsize, maxsize))
    
    return img2
def save(name,data):
    imwrite(dst+name,data)
def main():
    a=get_image()
    b=[]
    for i in a:
        b.append(process(src+i))
    for i in range(len(a)):
        save(a[i],b[i])

helptext="Usage: python square.py srcdir [dstdir]\nCrop and fit images to 64x64, from srcdir to dstdir, using OpenCV"
if __name__=="__main__":
    if len(sys.argv)<2:
        print(helptext)
        sys.exit(0)
    src=sys.argv[1]
    dst=sys.argv[2]if len(sys.argv)>2 else src 
    main()