## 项目亮点

- **易于使用**：专为新手设计的用户友好界面和详细的文档。
- **高效训练**：只需少量聊天数据，即可快速生成高质量的聊天机器人。支持全自动训练。
- **个性化**：能够训练出模拟你自己或任何其他现实或虚拟角色的聊天机器人。
- **强大性能**：基于最新的glm4开源模型，确保生成的对话自然、流畅且具有高度的互动性。
- **资源友好**：使用lora训练方法，家用级显卡，只要满足24G显存。都可以训练。
  
## 环境要求

请确保您的系统中已安装CUDA和PyTorch。
CUDA建议11.8以上
PyTochy建议2.0.0以上

### 创建虚拟环境

```
conda create -n Chatbot-Trainer python=3.10 -y
source activate Chatbot-Trainer
```

# 依赖安装
```
pip install -r requirements.txt
```

# 模型下载
```
pip install codewithgpu
cg down xxxiu/glm-4-9b-chat
```

## 模型推理测试

测试是否可以推理成功：
```
python test.py
```
## 训练

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
问：你叫(名字)，用这种说话方式和我对话
答：我平时一般工作完，就看看视频或者出门跑跑步，周末会去和朋友吃烧烤或者火锅。

问：你叫(名字)，用这种说话方式和我对话
答：诶呀。外面太热了，不想出门。
```

第二种数据集格式，优势在于无需传统一问一答的编写格式，无需根据问题提供回答。只要在"答"的后面跟着的是说话人说话的内容就行。
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

# 开始训练


```
python finetune.py  data/  glm-4-9b-chat  configs/lora.yaml
```


# 推理
```
python run.py
```

## 许可协议

+ 使用GLM-4 模型权重需要遵循 [模型协议](https://huggingface.co/THUDM/glm-4-9b/blob/main/LICENSE)。

+ 本开源仓库代码遵循 [Apache 2.0](LICENSE) 协议。


### 讨论学习

QQ群：296483610
微信公众号：AI会思考
（公众号里我会经常分享我最新的训练理解和微调信息差）
