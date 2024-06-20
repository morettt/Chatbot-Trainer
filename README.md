## 项目特点

- **易于使用**：专为新手设计的用户友好界面和详细的文档。
- **高效训练**：只需少量聊天数据，即可快速生成高质量的聊天机器人。
- **个性化**：能够训练出模拟你自己或任何其他现实或虚拟角色的聊天机器人。
- **强大性能**：基于最新的 LLM 技术，确保生成的对话自然、流畅且具有高度的互动性。

## 环境设置

请确保你已经安装了 CUDA 和 PyTorch。

### 创建虚拟环境

#### Linux:
```
conda create -n Chatbot-Trainer python=3.10 -y
source activate Chatbot-Trainer
```
#### Windows:
```
conda create -n Chatbot-Trainer python=3.10 -y
conda activate Chatbot-Trainer
```

#下载依赖
```
cd role-training
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#下载模型
```
cg down xxxiu/glm-4-9b-chat
```
尝试推理模型，观察是否可以推理成功：


开始训练

首先数据集制作分为两种，一种为传统的问答对格式。另一种为“半”监督格式。

问答对格式示例：
```
问：你叫什么？
答：你管我叫什么？我叫xxx

问：最近新出来了个电影，要去看吗？
答：诶呀。外面太热了，不想出门。
```
下面一种是“半”监督数据集
```
问：你叫xxx，用这种说话方式和我对话
答：你管我叫什么？我叫你xxx

问：你叫xxx，用这种说话方式和我对话
答：诶呀。外面太热了，不想出门。
```
第二种数据集格式，测试实际上只比第一种质量下降10%~20%左右，十分省力。只要保证“答”的部分里面的内容是你自己的说话风格就行了。
什么内容都可以。这里训练的主要就是你语言习惯。

数据集数量至少得有70对，这是最基础训练的基准。

将数据集保存好之后，即可开始训练，训练为全自动。无需手动配置参数：

运行此指令处理数据集：
```
python preprocessing.py
```
linux:
```
python finetune.py  data/  /root/Chatbot-Trainer/glm-4-9b-chat  configs/lora.yaml
```
windows:
```
python finetune.py  data\\  Chatbot-Trainer\\glm-4-9b-chat  Chatbot-Trainer\\configs\\lora.yaml
```

推理
```
python run.py
```
## 协议

+ 本开源仓库的代码则遵循 [Apache 2.0](LICENSE) 协议。



