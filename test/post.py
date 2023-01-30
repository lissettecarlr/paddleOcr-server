import requests
import time
import json
import os

URL = "http://127.0.0.1:6666/ocr/server"

IMAGE_NAME = "9.jpg"
LANGUAGE = "JAP"



def post() :
    data = {
        "ImagePath": os.path.join(os.getcwd(), IMAGE_NAME),
        "Language": LANGUAGE
    }
    proxies = {"http": None, "https": None}
    try :
        res = requests.post(URL, data=json.dumps(data), proxies=proxies)
        print("res={}".format(res))
        res.encoding = "utf-8"
        result = json.loads(res.text)
        print("result={}".format(result))
        content = ""
        for val in result["Data"]:
            print("val={}".format(val))
            content += val["Words"] + " "
        print(content)
    except Exception :
        print(result["Message"])



def main() :
    number = 3
    timeCount = 0
    for num in range(number) :
        start = time.time()
        post()
        end = time.time()
        timeCount += end - start
        print("time: {}\n".format(end - start))
    print("avg time: {}".format(timeCount / number))


if __name__ == "__main__" :
	main()
	