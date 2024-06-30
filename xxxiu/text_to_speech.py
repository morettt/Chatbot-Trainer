import io
import requests
import urllib.parse
from pydub import AudioSegment
from pydub.playback import play

class TextToSpeech:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_speech_from_text(self, text, id=1, segment_size=30, batch_size=50, temperature=1, top_k=5, top_p=1, speed=0.9,
                             seed=-1, audio_format="wav", preset="default", prompt_text=None, prompt_lang="auto", refer_wav_path="B:\\gpt-vits-api-kelong\\vits-simple-api\wav\\www.wav"):
        # 正确编码refer_wav_path
        encoded_refer_wav_path = urllib.parse.quote(refer_wav_path)
        params = {
            "segment_size": segment_size,
            "text": text,
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temperature,
            "batch_size": batch_size,
            "seed": seed,
            "id": id,
            "speed": speed,
            "format": audio_format,
            "preset": preset,
            "prompt_text": prompt_text,
            "prompt_lang": prompt_lang,
            "refer_wav_path": encoded_refer_wav_path  # 使用正确编码的路径
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            audio_data = io.BytesIO(response.content)
            return AudioSegment.from_file(audio_data, format=audio_format)
        else:
            raise Exception("请求失败:", response.status_code)

    @staticmethod
    def play_audio(audio):
        play(audio)

    def text_to_speech_and_play(self, text, preset="default", prompt_text=None, prompt_lang="auto", refer_wav_path="I:\\下载 (1).wav"):
        audio = self.get_speech_from_text(text, preset=preset, prompt_text=prompt_text, prompt_lang=prompt_lang, refer_wav_path=refer_wav_path)
        self.play_audio(audio)

if __name__ == "__main__":
    tts = TextToSpeech("http://192.168.231.15:23456/voice/gpt-sovits")

    while True:
        text_to_speak = input("请输入你想要转化为语音的文本：")
        if text_to_speak.lower() == 'quit':
            break
        try:
            tts.text_to_speech_and_play(text_to_speak, preset="default", prompt_text="都红到耳朵根了，现在要是用嘴亲亲你的小脸蛋？", prompt_lang="auto", refer_wav_path="I:\\下载 (1).wav")
        except Exception as e:
            print(e)