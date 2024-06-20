## 项目亮点

- **易于使用**：专为新手设计的用户友好界面和详细的文档。
- **高效训练**：只需少量聊天数据，即可快速生成高质量的聊天机器人。
- **个性化**：能够训练出模拟你自己或任何其他现实或虚拟角色的聊天机器人。
- **强大性能**：基于最新的glm4开源模型，确保生成的对话自然、流畅且具有高度的互动性。
- 
## 环境配置

请确保您的系统中已安装CUDA和PyTorch。
CUDA建议11.8以上
PyTochy建议2.0.0以上

### 创建虚拟环境

#### 对于Linux用户：
```
conda create -n Chatbot-Trainer python=3.10 -y
source activate Chatbot-Trainer
```

#### 对于Windows用户：
```
conda create -n Chatbot-Trainer python=3.10 -y
conda activate Chatbot-Trainer
```

# 依赖安装
```
cd Chatbot-Trainer
pip install -r requirements.txt
```

# 模型下载
```
git clone https://www.modelscope.cn/ZhipuAI/glm-4-9b-chat.git && mv glm-4-9b-chat models/

```

# 模型推理测试
尝试推理模型，确认推理成功：

## 训练步骤

首先，数据集制作分为两种格式：传统问答对格式和“半”监督格式。

**问答对格式示例**：
```
问：你叫什么？
答：你管我叫什么？我叫xxx

问：最近新出来了个电影，要去看吗？
答：诶呀。外面太热了，不想出门。
```

**“半”监督数据集示例**：
```
问：你叫xxx，用这种说话方式和我对话
答：你管我叫什么？我叫你xxx

问：你叫xxx，用这种说话方式和我对话
答：诶呀。外面太热了，不想出门。
```

第二种数据集格式，实际测试中质量仅比第一种下降10%~20%，操作简便。只需确保“答”的部分内容符合您的个人说话风格即可。内容不限，主要目的是训练您的语言习惯。

数据集至少包含70对问答，这是基础训练的最低标准。

数据集准备好后，即可开始全自动训练，无需手动配置参数：

**数据集预处理**：
```
python preprocessing.py
```

**Linux系统**：
```
python finetune.py  data/  /root/Chatbot-Trainer/glm-4-9b-chat  configs/lora.yaml
```

**Windows系统**：
```
python finetune.py  data\\  Chatbot-Trainer\\glm-4-9b-chat  Chatbot-Trainer\\configs\\lora.yaml
```

# 推理
```
python run.py
```

## 许可协议

+ 本开源仓库代码遵循 [Apache 2.0](LICENSE) 协议。
