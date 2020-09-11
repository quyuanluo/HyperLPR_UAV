import sys
import os
import time
from PIL import Image
import HyperLPRLite as pr
from cv2 import cv2
import numpy as np

SEND_FOLDER='images_lib/6/'


def ImageProcess(image_path):
    model = pr.LPR("model/cascade.xml","model/model12.h5","model/ocr_plate_all_gru.h5")
    grr = cv2.imread(image_path)
    print( "[Server] 神经网络正在处理图片.......")
    
    # 训练结果，为一个列表，其中每一个元素是包括字符串、自信度和车牌位置的列表
    # 如[['9F72E1', 0.6781167685985565, [145.62, 217.5, 104.53178023338317, 39.0]], 
    #    ['苏E9F72E', 0.8783870339393616, [107.66, 215.05, 140.35348415374756,42.9]]]
    proc_results=model.SimpleRecognizePlateByE2E(grr) 
    # 定义一个去掉结果中的位置信息的变量
    proc_results_without_pos=[]
    print( "[Server] 处理结果为：")
    for result in proc_results:
        print("plate_str:",result[0],"plate_confidence:",result[1])
        result.pop() #去掉结果中的位置信息，位于最后
        proc_results_without_pos.append(result)

    print("[Server] 正在计算处理时间......")
    t0 = time.time()
    for x in range(20):
        model.SimpleRecognizePlateByE2E(grr)
    t = (time.time() - t0)/20.0
    print("Image size: " + str(grr.shape[1])+"x"+str(grr.shape[0]) +  " need " + str(round(t*1000,2))+"ms")
    
    return proc_results_without_pos,t



if __name__ == '__main__': 
    # 在主函数中，先打开图像处理模型，然后可以不断输入图像进行处理
    # 不要每次需要图像处理时在打开，这样会报错，而且浪费时间
    # model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5") 
    # while True:
    time_set=[]
    posibility_set=[]
    files=os.listdir(SEND_FOLDER)
    i=0
    for file_name in files:
        #file_name=input("file name you want to process:")
        print("image******{}*****".format(i))
        i+=1
        results,proc_time=ImageProcess(SEND_FOLDER+file_name)
        if len(results):
            time_set.append(proc_time)
            posibility_set.append(results[-1][-1])

    time_set=np.array(time_set)  #将list转化为numpy
    posibility_set=np.array(posibility_set)
    time_set=time_set*1000  # 时间转化为秒

    # 将两个列表合二为一个numpy数组
    results_data=np.c_[time_set,posibility_set]
    np.savetxt('results_data.cvs',results_data,delimiter=',')

