import os
from funasr import AutoModel

# 设置模型
asr = "/root/autodl-tmp/xxxiu-asr2"
model = AutoModel(model=asr, model_revision="v2.0.4",
                 vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                 punc_model="/root/autodl-tmp/ct-punc", punc_model_revision="v2.0.4",
                 )

# 设置输入输出路径
input_dir = '/root/Chatbot-Trainer/音频'
output_dir = '/root/Chatbot-Trainer/输出文本'
output_file = os.path.join(output_dir, '输入内容.txt')

# 如果输出目录不存在，创建目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取所有wav和mp3文件并排序
audio_files = []
for file in os.listdir(input_dir):
    if file.lower().endswith(('.wav', '.mp3')):
        audio_files.append(os.path.join(input_dir, file))

# 自定义排序函数，提取文件名中的数字进行排序
def get_number(filename):
    try:
        return int(os.path.splitext(os.path.basename(filename))[0])
    except ValueError:
        return filename

# 按数字大小排序
audio_files.sort(key=get_number)

# 打开输出文件，准备写入所有结果
with open(output_file, 'w', encoding='utf-8') as f:
    # 处理每个音频文件
    total_files = len(audio_files)
    for index, audio_file in enumerate(audio_files, 1):
        print(f"\n正在处理第 {index}/{total_files} 个文件: {os.path.basename(audio_file)}")
        
        # 语音识别
        res = model.generate(input=audio_file, batch_size_s=120)
        
        # 写入结果
        if isinstance(res, list):
            for item in res:
                if isinstance(item, dict):
                    text = item.get('text', '')
                    f.write(text + '\n')
        else:
            f.write(str(res) + '\n')

print("\n音频已转换成功，请前往路径：Chatbot-Trainer/输出文本/输入内容.txt 查看")