import uuid
import json
import time
import requests

url = "https://nls-gateway.cn-shanghai.aliyuncs.com"

# AccessKey ID和AccessKey Secret
access_key_id = ""
access_key_secret = ""

# API密钥
api_key = ""

# 音频文件路径
audio_file = "output.mp3"

# 语音识别结果保存路径
result_file = "output.srt"

# 生成API请求参数
request_params = {
    "Format": "mp3",
    "Rate": "16000",
    "Volume": "0",
    "SpeechRate": "5",
    "PitchRate": "5",
    "EnableWordInfo": "false",
    "EnableSentenceInfo": "false",
    "EnableAudioTrack": "false",
    "Callback": "https://nls-gateway.cn-shanghai.aliyuncs.com",
    "CallbackContext": str(uuid.uuid4()),
    "CallbackType": "POST",
    "AppKey": api_key,
    "SpeechTimeout": "60000"
}

# 发起语音识别请求
with open(audio_file, "rb") as f:
    response = requests.post(url + "/v1/asr/async?Format=mp3&Rate=16000&Volume=0&SpeechRate=5&PitchRate=5&EnableWordInfo=false&EnableSentenceInfo=false&EnableAudioTrack=false&Callback=https://nls-gateway.cn-shanghai.aliyuncs.com&CallbackContext=59546186-d6a8-11e9-80b5-0016e069061f&CallbackType=POST&AppKey=27731260&SpeechTimeout=60000", data=f, headers={"Content-Type": "application/octet-stream"})

# 获取请求ID
request_id = json.loads(response.text)["RequestId"]

# 打印识别结果
def print_result():
    result = json.loads(requests.get(url + "/v1/asr/getasyncjobresult", params={"JobId": request_id}).text)
    with open(result_file, "w") as f:
        f.write("0\n")
        for item in result["Data"]["WordsInfo"]:
            f.write("{}\n".format(item["Word"]))

# 等待识别结果
while True:
    if json.loads(requests.get(url + "/v1/asr/checkasyncjobstatus", params={"JobId": request_id}).text)["Data"]["Status"] == "success":
        print_result()
        break
    else:
        print("识别中...")
        time.sleep(1)