# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
#  语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html
#  webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
#  语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
#  设置热词
#  注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
#  语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
#  可添加语种或方言，添加后会显示该方言的参数值
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import pyaudio
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
from ws4py.client.threadedclient import WebSocketClient
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


#  iat parameter
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

# 采样率
RATE = 16000
# 单声道
CHANNELS = 1
# 16bit编码格式
FORMAT = pyaudio.paInt16
# 一个缓冲区存放的帧数
CHUNK = 520


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat",
                             "language": "zh_cn",  # zh_cn, en_us
                             "accent": "mandarin",
                             "vinfo": 1,
                             "vad_eos": 3000,
                             'dwa': 'wpgs'} # 启动动态修正功能，纠正识别结果中的一些错误

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


class RecognitionWebsocket(WebSocketClient):
    def __init__(self, url, ws_param):
        super().__init__(url)
        self.ws_param = ws_param
        self.rec_text = {}

    # 收到websocket消息的处理
    def received_message(self, message):
        message = message.__str__()
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            status = json.loads(message)['data']['status']
            if code != 0:
                errMsg = json.loads(message)["message"]
                logging.error('sid:%s call error:%s code is:%s' % (sid, errMsg, code))
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)['data']['result']
                ws = data['ws']
                pgs = data['pgs']
                sn = data['sn']
                result = ''
                for i in ws:
                    for w in i['cw']:
                        result += w['w']
                if pgs == 'rpl':
                    rg = data['rg']
                    self.rec_text.update({rg[0]: result})
                    for i in range(rg[0] + 1, rg[1]):
                        self.rec_text.pop(i, '404')
                else:
                    self.rec_text[sn] = result
                logging.info('识别结果为: {}'.format(self.rec_text))
                # print("sid:%s call success!,data is:%s" % (sid, self.rec_text))
                # print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))

        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, error):
        print("### error:", error)
        logging.error(error)

    # 收到websocket关闭的处理
    def closed(self, code, reason=None):
        logging.info('语音识别通道关闭' + str(code) + str(reason))

    # 收到websocket连接建立的处理
    def opened(self):
        def run(*args):
            frameSize = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
            # 创建一个pyaudio实例对象
            p = pyaudio.PyAudio()
            # 打开一个流
            stream = p.open(rate=RATE,
                            channels=CHANNELS,
                            format=FORMAT,
                            input=True,
                            frames_per_buffer=CHUNK)
            print('开始识别------')

            # rate / chunk * record_time
            # 16000 / 1024 * 60 = 937.5
            for i in range(0, int(RATE / CHUNK * 10)):  # 一次发送10s的音频
                # 从流中读取chunk个字节的数据
                buf = stream.read(CHUNK)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:
                    d = {"common": self.ws_param.CommonArgs,
                         "business": self.ws_param.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    self.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    self.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    self.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                # time.sleep(intervel)

            # 暂停流
            stream.stop_stream()
            # 关闭流
            stream.close()
            # 关闭pyaudio
            p.terminate()
            self.close()

        thread.start_new_thread(run, ())


def run():
    wsParam = Ws_Param(APPID='d27586e0', APISecret='ZjMzYTljZTI2YzRkYmM5YjhlMmUxNGUw',
                       APIKey='4db3b33785190ede2ca85e6b51ff2fcf',
                       AudioFile=r'iat_pcm_16k.pcm')
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = RecognitionWebsocket(wsUrl, wsParam)
    ws.connect()
    ws.run_forever()
    # ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    time1 = datetime.now()
    run()
    time2 = datetime.now()
    print(time2 - time1)
