def process_all_dialogue(input_file, output_file):
    # 步骤1：读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 步骤2：替换A/B为问答格式并合并多行
    processed_lines = []
    current_qa = ""
    in_qa = False
    
    for line in lines:
        # 替换A/B为问答格式
        line = line.strip()
        line = line.replace('A:', '问：').replace('A：', '问：')
        line = line.replace('B:', '答：').replace('B：', '答：')
        
        if line.startswith('《分割》'):
            if current_qa:
                processed_lines.append(current_qa)
                current_qa = ""
            processed_lines.append('')  # 使用空行替代《分割》
            in_qa = False
        elif line.startswith('问：'):
            if current_qa:
                processed_lines.append(current_qa)
            current_qa = line
            in_qa = True
        elif line.startswith('答：'):
            if current_qa:
                processed_lines.append(current_qa)
            current_qa = line
            in_qa = True
        elif line and in_qa:
            current_qa += " " + line
        else:
            if current_qa:
                processed_lines.append(current_qa)
                current_qa = ""
            if line:
                processed_lines.append(line)
            in_qa = False
    
    if current_qa:
        processed_lines.append(current_qa)
    
    # 步骤3：写入最终文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in processed_lines:
            if line.strip():
                f.write(line + '\n')
            else:
                f.write('\n')  # 保留空行

# 使用代码
input_path = '/root/Chatbot-Trainer/输出文本/合集/处理后分割文本.txt'
output_path = '/root/Chatbot-Trainer/输出文本/合集/最终问答文本.txt'

try:
    process_all_dialogue(input_path, output_path)
    print("所有处理完成！最终文件已保存至:", output_path)
except Exception as e:
    print("处理过程中出现错误:", str(e))