import json

def process_and_transform_file(input_path, output_path):
    try:
        dialogue_blocks = []
        current_dialogue = []
        system_prompt = None

        with open(input_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line == "":
                    if current_dialogue:
                        if system_prompt:
                            current_dialogue.insert(0, system_prompt)
                        dialogue_blocks.append({"messages": current_dialogue})
                        current_dialogue = []
                        system_prompt = None
                    continue

                if line.startswith("前缀："):
                    system_prompt = {
                        "role": "system",
                        "content": line[3:].strip()
                    }
                elif line.startswith("问："):
                    current_dialogue.append({"role": "user", "content": line[2:].strip()})
                elif line.startswith("答："):
                    current_dialogue.append({"role": "assistant", "content": line[2:].strip()})

        if current_dialogue:
            if system_prompt:
                current_dialogue.insert(0, system_prompt)
            dialogue_blocks.append({"messages": current_dialogue})

        with open(output_path, 'w', encoding='utf-8') as output_file:
            for entry in dialogue_blocks:
                output_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

        print(f"转换完成，并已保存至：{output_path}")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")

# 指定原始文件路径和输出文件路径
input_path = "/root/Chatbot-Trainer/输出文本/合集/最终问答文本.txt"
output_path = "/root/Chatbot-Trainer/data/train.jsonl"

# 调用函数处理文件
process_and_transform_file(input_path, output_path)