def process_text(input_file_path, output_file_path, sentences_per_paragraph=7):
    # 读取文件内容并移除换行符
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace('\n', '')

    # 初始化变量
    paragraph = []
    sentence_count = 0
    paragraphs = []

    # 分割文本为句子并分组成段落
    for sentence in content.split('。'):
        if sentence:  # 忽略空句子
            paragraph.append(sentence + '。')
            sentence_count += 1
            if sentence_count >= sentences_per_paragraph:
                paragraphs.append('《分割》\n' + ''.join(paragraph))
                paragraph = []  # 重置段落
                sentence_count = 0

    # 添加最后一个段落（如果有）
    if paragraph:
        paragraphs.append('《分割》\n' + ''.join(paragraph))

    # 写入处理后的文本到新文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for paragraph in paragraphs:
            file.write(paragraph + '\n\n')

    print('处理完成')


# 定义文件路径
input_file_path = '/root/Chatbot-Trainer/输出文本/输入内容.txt'
output_file_path = '/root/Chatbot-Trainer/输出文本/合集/合集.txt'

# 调用函数
process_text(input_file_path, output_file_path)
