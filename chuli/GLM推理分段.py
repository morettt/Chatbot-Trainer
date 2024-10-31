# -*- coding: utf-8 -*-
import os
import requests
import json

def chat_with_gpt3_5(user_input, max_retries=3):
    system_message = {
        "role": "system",
        "content": "请帮我把这段独白转成A/B对话格式。要求：1.所有原文内容必须放在B的发言里！A只能回应顺着话题说！2.A负责引导对话用提问带出话题,B保证有一定的原有口语表达，或者稍做修改使对话更有逻辑,但前提是不要改变原文说话人的语气风格。例文：小美人鱼这电影难看,CG差,但歌还行。应转成 A:看了小美人鱼感觉如何？B:小美人鱼这电影难看,CG差。A:都不好吗？B:但歌还行。请处理以下内容："
    }
    
    payload = {
        "prompt": user_input,
        "history": [[system_message["content"], None]],
        "max_length": 4000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                "http://0.0.0.0:6006",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60  # 设置超时时间为60秒
            )
            response.raise_for_status()  # 如果响应状态码不是200，将引发异常
            
            # 处理SSE流式响应
            response_text = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        if 'response' in data:
                            response_text += data['response']
                        elif 'end_of_stream' in data:
                            break
            
            return response_text

        except requests.exceptions.RequestException as e:
            print(f"处理问题时出错，尝试次数：{attempt}/{max_retries}")
            print(f"详细错误信息: {str(e)}")
            print(f"响应状态码: {getattr(e.response, 'status_code', 'No response')}")
            print(f"响应内容: {getattr(e.response, 'text', 'No response')}")
            
            if attempt == max_retries:
                return f"重试{max_retries}次后仍然失败，错误信息：{str(e)}"

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

def main():
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

if __name__ == "__main__":
    main()