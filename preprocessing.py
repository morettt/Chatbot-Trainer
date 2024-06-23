import re
import json
import random
import os

def format_and_transform_text(input_file_path, intermediate_file_path):
    """处理和格式化文本，转换成JSONL格式"""
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到。")
        return

    questions = re.split(r'问[：:]\s*', content)[1:]
    intermediate_data = []

    for q in questions:
        if re.search(r'答[：:]\s*', q):
            parts = re.split(r'答[：:]\s*', q, 1)
            question, answer = parts[0].strip(), parts[1].strip()
            answer = answer.replace('\n', ' ')
            answer = re.sub(r'(\d+)\.', r' \1.', answer)
            intermediate_data.append({"prompt": question, "response": answer})
        else:
            intermediate_data.append({"prompt": q.strip(), "response": ""})

    try:
        with open(intermediate_file_path, 'w', encoding='utf-8') as output_file:
            for entry in intermediate_data:
                transformed_data = {
                    "messages": [
                        {"role": "user", "content": entry["prompt"]},
                        {"role": "assistant", "content": entry["response"]}
                    ]
                }
                output_file.write(json.dumps(transformed_data, ensure_ascii=False) + '\n')
    except IOError:
        print(f"无法写入文件 {intermediate_file_path}。")

def select_random_samples(data, num_samples=50):
    """从数据中随机选择指定数量的样本"""
    return random.sample(data, min(num_samples, len(data)))

def save_samples_to_file(samples, output_file_path):
    """将选中的样本保存到文件"""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for item in samples:
                json.dump(item, file, ensure_ascii=False)
                file.write('\n')
    except IOError:
        print(f"无法写入文件 {output_file_path}。")

def create_dev_json_from_train_json(train_file_path, dev_file_path, num_samples=50):
    """从train.json中随机选择样本并保存到dev.json"""
    try:
        with open(train_file_path, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
    except FileNotFoundError:
        print(f"文件 {train_file_path} 未找到。")
        return
    except json.JSONDecodeError:
        print(f"文件 {train_file_path} 格式错误。")
        return

    selected_samples = select_random_samples(data, num_samples)
    save_samples_to_file(selected_samples, dev_file_path)

if __name__ == "__main__":
    source_file_path = os.path.abspath('dataset/QA.txt')
    train_file_path = os.path.abspath('data/train.jsonl')
    dev_file_path = os.path.abspath('data/dev.jsonl')
    num_samples = 50

    # 确保data目录存在
    os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(dev_file_path), exist_ok=True)

    # Process and format text to JSONL
    format_and_transform_text(source_file_path, train_file_path)

    # Create dev.json from train.json
    create_dev_json_from_train_json(train_file_path, dev_file_path, num_samples)
