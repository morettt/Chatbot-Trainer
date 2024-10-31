import json
import random
import os

def load_data(file_path):
    """加载JSON格式的数据文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data

def select_random_samples(data, num_samples=50):
    """从数据中随机选择指定数量的样本"""
    return random.sample(data, min(num_samples, len(data)))

def save_samples_to_file(samples, output_file_path):
    """将选中的样本保存到文件"""
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for item in samples:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

def create_dev_json_from_train_json(input_file_path, output_file_path, num_samples=50):
    """从train.json中随机选择样本并保存到dev.json"""
    data = load_data(input_file_path)
    selected_samples = select_random_samples(data, num_samples)
    save_samples_to_file(selected_samples, output_file_path)
    print(f"已成功保存选中的记录到 {output_file_path}")

if __name__ == "__main__":
    train_json_path = "/root/Chatbot-Trainer/data/train.jsonl"  # 训练集文件路径
    dev_json_path = "/root/Chatbot-Trainer/data/dev.jsonl"  # 保存开发集的目标文件路径
    num_samples = 50  # 从训练集中选取的样本数量

    create_dev_json_from_train_json(train_json_path, dev_json_path, num_samples)
