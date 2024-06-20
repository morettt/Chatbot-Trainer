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
git clone https://www.modelscope.cn/ZhipuAI/glm-4-9b-chat.git
```

打开run.py文件，找到这行代码：MODEL_PATH = os.environ.get('MODEL_PATH', '模型路径')
将其中的“模型路径”替换为你刚刚下载的glm-4-9b-chat模型的绝对路径。并保存


## 模型推理测试

测试是否可以推理成功：
```
python run.py
```
## 开始训练

首先，数据集制作分为两种格式：传统问答对格式和“半”监督格式。

**问答对格式示例**：
```
问：你平时一般做什么呀？
答：我平时一般工作完，就看看视频或者出门跑跑步，周末会去和朋友吃烧烤或者火锅。

问：最近新出来了个电影，要去看吗？
答：诶呀。外面太热了，不想出门。
```

**“半”监督数据集示例**：
```
问：你叫某某某，用这种说话方式和我对话
答：我平时一般工作完，就看看视频或者出门跑跑步，周末会去和朋友吃烧烤或者火锅。

问：你叫某某某，用这种说话方式和我对话
答：诶呀。外面太热了，不想出门。
```

第二种数据集格式，优势在于无需传统一问一答的编写格式，无需修改"问"的部分。只要在"答"的后面跟着的是说话人说话的内容就行。
甚至不需要有一定的逻辑。只需确保“答”的部分内容符合您的个人说话风格或者训练人说话风格即可。什么内容都可以，这里主要是训练您的语言习惯。
在实际的测试中第二种方法仅比第一种下降10%~20%的模型质量，操作简便。

但即便如此，数据集还是至少包含70对问答，如果想要有好的效果，这是最低标准。

## 数据集制作

我在dataset里面放了一个"半监督QA"和一个"QA"文件。你可以选择你希望训练的数据集格式
如果打算用QA文本训练，数据集里面有大约100条问题，你需要用你自己的性格和语气来一一回复这些问题，写在“答”后面。
全部写完后，记得保存。

然后再运行这个指令处理你刚刚编写的数据集：

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
