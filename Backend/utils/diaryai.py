import openai
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
# 创建一个Recognizer对象
r = sr.Recognizer()


# 使用speech_recognition录音
def record_audio(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        r.adjust_for_ambient_noise(source, duration=0.5)  # 动态调整能量阈值以解决环境噪声（自动调整静音检测的阈值）（使用后可显著提高效果）
        audio = r.listen(source, phrase_time_limit=59)  # 限制录音的最长时长为59秒，防止超出百度的时间限制
        print('record finish')

    with open("voice.wav", "wb") as f:
        f.write(audio.get_wav_data())

    return audio


text = '识别失败'

# 设置 API Key，申请地址：https://platform.openai.com/account/api-keys
openai.api_key = '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'
# 设置组织，查看地址：https://platform.openai.com/account/org-settings
openai.organization = "org-MmExD0t6JKxXSrxJCLhXdTVd"
while True:
    record_audio()

    # 将语音转换为文本
    try:
        # text = r.recognize_google(audio, language='zh-CN')
        audio_file = open("voice.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        text = transcript["text"]
        print("你说的是：" + text)

    except sr.UnknownValueError:
        print("无法识别你的语音")
        continue
    except sr.RequestError as e:
        print("无法连接到Google API，错误原因：" + str(e))
        continue

    engine.say(f'收到, 你说的是{text}')
    engine.runAndWait()
