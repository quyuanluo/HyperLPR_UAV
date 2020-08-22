import sys
import os
from PIL import Image
import HyperLPRLite as pr
import cv2
import numpy as np
import time

def SpeedTest(image_path):
    grr = cv2.imread(image_path)
    model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
    model.SimpleRecognizePlateByE2E(grr)
    t0 = time.time()
    for x in range(20):
        model.SimpleRecognizePlateByE2E(grr)
    t = (time.time() - t0)/20.0
    print("Image size :" + str(grr.shape[1])+"x"+str(grr.shape[0]) +  " need " + str(round(t*1000,2))+"ms")

    
filePath = "images_lib/1/"
files=os.listdir(filePath)
model = pr.LPR("model/cascade.xml","model/model12.h5","model/ocr_plate_all_gru.h5")
for file in files:
    grr = cv2.imread(filePath + file)
    print( "imgname---"+file)
    for pstr,confidence,rect in model.SimpleRecognizePlateByE2E(grr):
            if confidence>0.1:
                print("plate_str:",pstr,"plate_confidence:",confidence)

cv2.waitKey(0)

SpeedTest(filePath+"1.jpg")
