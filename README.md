# HyperLPR-simple
## 本项目的环境为：
### Ubuntu 16.04 LTS 
### Python==3.5.2

#### 图像处理程序所需要的包为:

tensorflow==1.13.1

Keras==2.3.1

numpy==1.18.5

scipy==1.4.1

opencv-python==4.3.0.38

Scikit-image==0.15.0

Pillow==7.2.0

### 用于RESTful API的包
Flask==1.1.2 

requests==2.24.0

# 配置虚拟环境（可选项）
### virtualenv创建虚拟环境，主要用于在一台电脑上需要安装不同版本的python虚拟环境来做项目, virtualenv就是用来为一个项目创建一套可以隔离的Python运行环境。
#### 下载虚拟环境包
1. sudo pip3 install virtualenv (pip3将virtualenv装在python3下)
#### 创建环境
2. virtualenv -p /usr/bin/python3.5 myenv （python3.5是想加入虚拟环境的python版本，可以根据需要自己去/usr/bin目录下选择；myenv是自己创建放虚拟环境的文件夹）
#### 激活环境
3. source myenv/bin/activate
#### 推出虚拟环境
4. deactivate