import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# x 参数为numpy类型的数组
def draw_hist(x):
    sns.set()                                   #设置seaborn默认格式

    plt.rcParams['axes.unicode_minus']=False      #显示负号

    plt.rcParams['figure.figsize'] = (13, 5)    #设定图片大小
    f = plt.figure()                            #确定画布

    f.add_subplot(1,2,1)
    sns.distplot(x, kde=False)                 #绘制频数直方图
    plt.ylabel("numbers", fontsize=16)
    plt.xticks(fontsize=16)                    #设置x轴刻度值的字体大小
    plt.yticks(fontsize=16)                   #设置y轴刻度值的字体大小
    plt.title("(a)", fontsize=20)             #设置子图标题

    f.add_subplot(1,2,2)
    sns.distplot(x)                           #绘制密度直方图
    plt.ylabel("density", fontsize=16)
    plt.xticks(fontsize=16)                  #设置x轴刻度值的字体大小
    plt.yticks(fontsize=16)                  #设置y轴刻度值的字体大小
    plt.title("(b)", fontsize=20)            #设置子图标题

    plt.subplots_adjust(wspace=0.3)         #调整两幅子图的间距
    plt.show()

if __name__ == '__main__':

    # np.random.seed(0)                           #设置随机种子数
    # x = np.random.randn(100) 
    x=np.loadtxt("process_time")
    x=x*1000
    draw_hist(x)