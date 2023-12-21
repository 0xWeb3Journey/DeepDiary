import pyaudio

rate = 16000
channels = 1
format = pyaudio.paInt16
# 一个缓冲区存放的帧数
chunk = 1024
# 录音时间
record_time = 5

# 创建一个pyaudio实例对象
p = pyaudio.PyAudio()
# 打开一个流
stream = p.open(rate=rate, channels=channels,format=format,input=True)

# rate / chunk * record_time
# 16000 / 1024 * 60 = 937.5
for i in range(0, int(rate / chunk * record_time)):
    # 从流中读取chunk个字节的数据
    data = stream.read(chunk)
    # 将数据写入文件
    # wf.write(data)
    print(data)
# 暂停流
stream.stop_stream()
# 关闭流
stream.close()
# 关闭pyaudio
p.terminate()