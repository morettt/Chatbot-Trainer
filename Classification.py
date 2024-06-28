import openai
import os

# 安全设置 API 密钥和基地址
openai.api_key = 'sk-dSnGN0LKtXuiOIxI34C0EeB4773c468695C99e069c13013a'
openai.api_base = 'https://api.xty.app/v1'

def classify_answer(answer):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "你是一个情感分析助手，请根据以下句子进行分类，别说多余的话，只需输入：激动、正常、温柔。"},
            {"role": "user", "content": answer}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def process_file(input_file_path, output_file_base):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    results = {
        "激动": [],
        "正常": [],
        "温柔": []
    }

    # 每三行处理一次
    for i in range(0, len(lines), 3):
        if i+1 < len(lines) and lines[i].startswith('问：') and lines[i+1].startswith('答：'):
            question = lines[i].strip()  # 保持问题前缀"问："
            answer = lines[i+1].strip()  # 保持答案前缀"答："
            classification = classify_answer(answer[2:])  # 去掉"答："前缀进行分类
            # 处理非预期分类结果
            if classification not in results:
                print(f"Unexpected classification: {classification}. Defaulting to '未知分类'.")
                classification = "未知分类"
                if classification not in results:
                    results[classification] = []
            print(f"{question}\n{answer}\n分类结果：{classification}\n")  # 在命令行打印完整信息
            results[classification].append(f"{question}\n{answer}\n")  # 文件中写入保持原格式

    # 将分类结果写入对应的文件中
    for category, content in results.items():
        with open(f"{output_file_base}_{category}.txt", 'w', encoding='utf-8') as file:
            file.writelines(content)

# 示例文件路径和环境变量设置
input_file_path = '试验.txt'
output_file_base = '分类'

# 处理文件
process_file(input_file_path, output_file_base)
