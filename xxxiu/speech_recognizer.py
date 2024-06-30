import keyboard
import speech_recognition as sr
from aip import AipSpeech
import time


class SpeechRecognizer:
    def __init__(self, app_id, api_key, secret_key):
        self.client = AipSpeech(app_id, api_key, secret_key)
        self.recognizer = sr.Recognizer()
        self.rate = 16000

    def _record(self):
        with sr.Microphone(sample_rate=self.rate) as source:
            # 可选择是否需要调整环境噪音，如果环境通常较安静，可以省略这一步
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("按住'z'键开始讲话，松开停止")

            audio = None
            while True:
                if keyboard.is_pressed('z'):
                    print("正在录音...")
                    audio = self.recognizer.listen(source, timeout=60, phrase_time_limit=300)
                    print("录音结束")
                    break
                time.sleep(0.001)

            return audio.get_wav_data()

    def speech_to_text_baidu(self):
        result = self.client.asr(self._record(), 'wav', self.rate, {'dev_pid': 1537})

        if result["err_msg"] != "success.":
            return "语音识别失败：" + result["err_msg"]
        else:
            return result['result'][0]


if __name__ == "__main__":
    # 在实际使用中，建议将这些敏感信息存储在环境变量或配置文件中，而非硬编码在脚本里
    APP_ID = "64373851"
    API_KEY = "SrOB06t5Aeis9JUsLCtOqQ1G"
    SECRET_KEY = "UzfgCSptZ3WjEP7stYyNHXWsGikPgPka"

    speech_recognizer = SpeechRecognizer(APP_ID, API_KEY, SECRET_KEY)

    while True:
        try:
            result = speech_recognizer.speech_to_text_baidu()
            print(result)
        except Exception as e:
            print(f"Error occurred: {str(e)}")