import requests
import json
import cv2
from base64 import b64encode
from cv2 import imencode

URL = "http://127.0.0.1:6666/ocr/server"
IMAGE_NAME = "9.jpg"
LANGUAGE = "write"


def image_to_base64(image_np):
    #压缩
    image = imencode('.jpg', image_np)[1]
    image_code = str(b64encode(image))[2:-1]
    return image_code

def post() :
    #先打开image
    image =cv2.imread(IMAGE_NAME)
    #print(type(image))
    img = image_to_base64(image)

    proxies = {"http": None, "https": None}
    response = requests.post(URL, data={"image": img,"language": LANGUAGE}, proxies=proxies,timeout=20)
    if response:
        #print("本地OCR识别结果：".format(response))
        response.encoding = "utf-8"
        responseText = json.loads(response.text)
        print("responseText={}".format(responseText))
        result = responseText["Data"]

        for one_ann in result:
            text = one_ann["Words"]
            print("text={}".format(text))
            
if __name__ == "__main__" :
	post()
	