import openai
import json
import requests
import subprocess

# 设置OpenAI API基础URL
openai.api_base = "https://xqtd520qidong.com/v1/chat/completions"

# 模拟的外部函数，用于查询 IP 地址的地理位置
def get_location_by_ip(ip: str = None):
    if ip is None:
        # 如果没有提供 IP，使用 API 获取当前公网 IP
        response = requests.get('https://api.ipify.org')
        ip = response.text
    # 这里我们简化实际的 API 调用，只返回一个模拟地址
    return {"location": "模拟地址: 地球,太阳系"}

# 爬虫函数
def run_crawler() -> str:
    directory_path = "B:\\pachong\\MediaCrawler-main"
    # 批处理文件名
    batch_file = "一键调用.bat"
    try:
        # 构建执行命令，首先切换到指定目录，然后执行批处理文件
        command = f"cd /d {directory_path} && {batch_file}"
        # 使用 subprocess.Popen 在新的命令行窗口中启动批处理文件
        result = subprocess.Popen(["cmd.exe", "/c", command], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # 等待输入，以保持窗口开启
        input("按任意键结束...")
        return "爬虫程序成功执行：已在新的命令行窗口中启动进程。"
    except Exception as e:
        # 如果发生异常，返回一个错误消息
        return f"执行爬虫程序时出错：{str(e)}"

# 函数工具列表
tools = [
    {
        "name": "get_location_by_ip",
        "description": "获取当前的地址",
        "func": get_location_by_ip
    },
    {
        "name": "run_crawler",
        "description": "在新窗口中运行爬虫程序",
        "func": run_crawler
    }
]

# 主函数
if __name__ == '__main__':
    openai.api_key = "sk-PJXKjdcp53qLrKDYF0D28674A79a44A9Ac57B1Ac115c850f"
    messages = [
        {"role": "system", "content": "从现在开始，你要模仿一个傲娇大小姐和我聊天,可以根据用户的问题调用不同的函数工具来获取信息或执行操作。"}
    ]

    while True:
        user_input = input("您有什么问题吗? (输入'quit'退出) ")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        # 创建一个函数调用请求
        response = openai.ChatCompletion.create(
            model="claude-3-opus-20240229",  # 使用 GPT API
            messages=messages,
            functions=[{"name": tool["name"], "description": tool["description"]} for tool in tools],
            function_call="auto"
        )

        # 解析响应
        if "function_call" in response.choices[0].message:
            # 如果调用了函数工具
            function_name = response.choices[0].message["function_call"]["name"]
            function_args = json.loads(response.choices[0].message["function_call"]["arguments"])

            # 查找对应的函数并执行
            for tool in tools:
                if tool["name"] == function_name:
                    function_response = tool["func"](**function_args)
                    break

            # 将函数响应添加到消息列表
            messages.append(response.choices[0].message)
            messages.append({"role": "function", "name": function_name, "content": json.dumps(function_response)})

            # 发送第二次请求
            response = openai.ChatCompletion.create(
                model="claude-3-opus-20240229",  # 使用 GPT API
                messages=messages
            )

            print(response.choices[0].message.content)
        else:
            # 如果没有调用函数工具,直接输出响应
            print(response.choices[0].message.content)
