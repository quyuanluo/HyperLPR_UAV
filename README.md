# HyperLPR-simple
## 本项目的环境为：
### Ubuntu 16.04 LTS 
### Python==3.5.2

### 图像处理程序所需要的包为:

tensorflow==1.13.1

Keras==2.3.1

numpy==1.18.5

scipy==1.4.1

opencv-python==4.3.0.38

Scikit-image==0.15.0

Pillow==7.2.0

### 用于RESTful API的包
##### Flask==1.1.2 
##### requests==2.24.0

## Redis 相关配置
### 安装Python版的redis

pip install redis

### 下载Redis服务器包
$ sudo apt-get install redis-server
#### 启动 Redis
$ redis-server
#### 查看 redis 是否启动？
$ redis-cli
#### 以上命令将打开以下终端：

redis 127.0.0.1:6379>

127.0.0.1 是本机 IP ，6379 是 redis 服务端口。现在我们输入 PING 命令。

redis 127.0.0.1:6379> ping

PONG

#### 以上说明我们已经成功安装了redis。

### 设置远程Redis服务可以被访问（https://www.jianshu.com/p/0ed7e88325dd）
##### 通常来说，生产环境下的Redis服务器只设置为仅本机访问（Redis默认也只允许本机访问）。有时候我们也许需要使Redi能被远程访问。
#### 1 修改Redis配置文件/etc/redis/redis.conf，找到bind那行配置（Ubuntu系统是这个路径）
vim /etc/redis/redis.conf
#### 2 去掉#注释并改为：
bind 0.0.0.0

或者指定特定的IP才可以访问，可以一次指定多个，如 bind 192.10.1.1 192.10.1.2 192.10.1.3
#### 3 指定配置文件然后重启Redis服务：
sudo redis-server /etc/redis/redis.conf
#### 4 重启 redis 服务：
sudo service redis-server restart
### 远程连接
#### 配置好Redis服务并重启服务后。就可以使用客户端远程连接Redis服务了。命令格式如下：
redis-cli -h {redis_host} -p {redis_port}

#### 其中{redis_host}就是远程的Redis服务所在服务器地址，{redis_port}就是Redis服务端口（Redis默认端口是6379）。例如：
 $ redis-cli -h 120.120.10.10 -p 6379
 
redis>ping

PONG

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

## git 将本地项目关联到远程仓库 
### 1.首先在项目目录下初始化本地仓库

#### git init

### 2.添加所有文件( . 表示所有)

#### git add .

### 3.提交所有文件到本地仓库

#### git commit -m "备注信息"

### 4.连接到远程仓库

#### git remote add origin 你的远程仓库地址

### 5.将项目推送到远程仓库

#### git push -u origin master

### 常用命令 
#### 取回远程仓库的变化，并与本地分支合并
##### git pull
