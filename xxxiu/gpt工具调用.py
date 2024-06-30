import openai
import json
import webbrowser
import subprocess
from text_to_speech import TextToSpeech
from speech_recognizer import SpeechRecognizer

# API配置
APP_ID = "64373851"
API_KEY = "SrOB06t5Aeis9JUsLCtOqQ1G"
SECRET_KEY = "UzfgCSptZ3WjEP7stYyNHXWsGikPgPka"
speech_recognizer = SpeechRecognizer(APP_ID, API_KEY, SECRET_KEY)

openai.api_base = "https://api.xty.app/v1"
openai.api_key = "sk-pFIAXkeWzsVd83VbFcF79a65D49c48A5B3B996CcE8Db3411"

# 函数定义
def Turn_on_computer_camera(url):
    try:
        success = webbrowser.open(url)
        return "摄像头成功打开" if success else "无法打开摄像头"
    except Exception as e:
        return f"出现错误: {str(e)}"

def shutdown_computer():
    try:
        # 这里使用 Windows 的 `shutdown` 命令
        subprocess.Popen(["cmd.exe", "/c", "shutdown /s /t 0"], creationflags=subprocess.CREATE_NO_WINDOW)
        return "电脑已成功关机。"
    except Exception as e:
        return f"关机时出错：{str(e)}"



def run_crawler():
    directory_path = "B:\\pachong\\MediaCrawler-main"
    batch_file = "一键调用.bat"
    try:
        command = f"cd /d {directory_path} && {batch_file}"
        subprocess.Popen(["cmd.exe", "/c", command], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return "爬虫程序成功执行：已在命令行窗口中启动进程。"
    except Exception as e:
        return f"执行爬虫程序时出错：{str(e)}"

def run_the_QQ_application():
    directory_path = r"C:\Program Files\Tencent\QQNT"
    batch_file = "QQ.exe"
    try:
        subprocess.Popen(["cmd.exe", "/c", batch_file], cwd=directory_path, creationflags=subprocess.CREATE_NO_WINDOW)
        return "打开QQ成功。"
    except Exception as e:
        return f"打开QQ时出错：{str(e)}"

# 函数工具列表
tools = [
    {"name": "run_crawler", "description": "运行爬虫程序", "func": run_crawler},
    {"name": "run_the_QQ_application", "description": "在电脑上打开QQ", "func": run_the_QQ_application},
    {"name": "Turn_on_computer_camera", "description": "打开电脑摄像头", "func": Turn_on_computer_camera},
    {"name": "shutdown_computer", "description": "把电脑关机", "func": shutdown_computer},
]

# 主函数
if __name__ == '__main__':
    messages = [{"role": "system", "content": "下面，你要模仿一个聪明、傲娇、淘气的人和我对话"}]

    while True:
        user_input = speech_recognizer.speech_to_text_baidu()
        print(f"我说：{user_input}")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        # 创建一个函数调用请求
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            functions=[{"name": tool["name"], "description": tool["description"]} for tool in tools],
            function_call="auto"
        )

        # 解析响应
        if "function_call" in response.choices[0].message:
            function_name = response.choices[0].message["function_call"]["name"]
            function_args_json = response.choices[0].message["function_call"]["arguments"]

            if function_args_json:
                try:
                    function_args = json.loads(function_args_json)
                except json.JSONDecodeError:
                    print("接收到无效的 JSON 字符串。")
                    continue

                function_response = None
                for tool in tools:
                    if tool["name"] == function_name:
                        # 检查是否是需要特殊参数的函数
                        if tool["name"] == "Turn_on_computer_camera":
                            function_response = tool["func"]("http://192.168.200.238/mjpeg/1")
                        else:
                            function_response = tool["func"](**function_args)
                        break

                function_content = json.dumps(function_response) if function_response is not None else "空结果"
                messages.append({"role": "function", "name": function_name, "content": function_content})
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages
                )

                response_text = response.choices[0].message.content
            else:
                response_text = "没有收到需要执行的函数参数。"
        else:
            response_text = response.choices[0].message.content

        print(response_text)

        # 语音合成
        tts = TextToSpeech("http://192.168.200.15:23456/voice/gpt-sovits")
        tts.text_to_speech_and_play(response_text)
