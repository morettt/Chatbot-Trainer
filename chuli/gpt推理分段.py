# -*- coding: utf-8 -*-
import os
import openai
# 尝试从环境变量中获取API密钥，如果没有设置，使用硬编码的密钥
api_key = os.getenv('OPENAI_API_KEY', 'sk-OQpBW29cqHyrPpMt44F622EeB3B544CeAa28843d62F23b38')
openai.api_base = "https://chatapi.midjourney-vip.cn/v1"

def chat_with_gpt3_5(user_input, max_retries=3):
    system_message = {
        "role": "system",
        "content": "请帮我把这段独白转成A/B对话格式。要求：1.所有原文内容必须放在B的发言里！A只能回应顺着话题说！2.A负责引导对话用提问带出话题,B保证有一定的原有口语表达，或者稍做修改使对话更有逻辑,但前提是不要改变原文说话人的语气风格。例文：小美人鱼这电影难看,CG差,但歌还行。应转成 A:看了小美人鱼感觉如何？B:小美人鱼这电影难看,CG差。A:都不好吗？B:但歌还行。请处理以下内容："
    }
    user_message = {"role": "user", "content": user_input}
    
    for attempt in range(1, max_retries + 1):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[system_message, user_message],
                api_key=api_key,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4000,
                presence_penalty=0.0,
                frequency_penalty=0.0
            )
            assistant_reply = response['choices'][0]['message']['content']
            return assistant_reply
        except Exception as e:
            print(f"处理问题时出错，尝试次数：{attempt}/{max_retries}。错误信息：{e}")
            if attempt == max_retries:
                return f"重试{max_retries}次后仍然失败，错误信息：{e}"

def process_and_save_text(input_file, output_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用《分割》分隔文本
    segments = content.split('《分割》')
    
    # 处理每个分段
    for i, segment in enumerate(segments):
        # 跳过空段落
        if not segment.strip():
            continue
            
        print(f"\n开始处理第 {i} 段内容...")
        
        # 获取处理后的内容
        processed_content = chat_with_gpt3_5(segment.strip())
        
        # 准备写入的内容
        output_text = f"\n《分割》\n{processed_content}\n"
        
        # 输出到屏幕
        print(output_text)
        
        # 追加模式写入文件
        with open(output_file, 'a', encoding='utf-8') as out_file:
            out_file.write(output_text)
            
        print(f"第 {i} 段内容已处理完成并保存")

# 文件路径
input_file = "/root/Chatbot-Trainer/输出文本/合集/合集.txt"
output_file = "/root/Chatbot-Trainer/输出文本/合集/处理后分割文本.txt"

# 确保输出文件是空的
with open(output_file, 'w', encoding='utf-8') as f:
    pass

# 处理文本并保存
print("开始处理文件...")
process_and_save_text(input_file, output_file)
print("\n所有内容处理完成！")