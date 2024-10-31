#!/bin/bash

# 定义依赖安装标志文件的路径
DEP_INSTALLED_FLAG="/root/Chatbot-Trainer/chuli"

# 激活环境
source activate api

# 检查是否已经安装过依赖
if [ ! -f "$DEP_INSTALLED_FLAG" ]; then
    # 如果标志文件不存在，表明是第一次运行，需要安装依赖
    cd /root/Chatbot-Trainer/chuli
    pip install -r xxx.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    # 安装完成后，创建标志文件
    touch "$DEP_INSTALLED_FLAG"
fi

python /root/Chatbot-Trainer/chuli/跨域API.py
