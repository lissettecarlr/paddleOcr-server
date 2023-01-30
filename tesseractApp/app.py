import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"

from flask import Flask, request, jsonify
from traceback import print_exc
import json
import uuid
from loguru import logger

from tesseractOcr import tesseractOcr
tesseract = tesseractOcr()


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# 失败的返回
def jsonFail(message):
    post_data = {
        "Code": -1,
        "Message": str(message),
        "RequestId": str(uuid.uuid4())
    }
    return jsonify(post_data)


# 成功的返回
def jsonSuccess(data):
    post_data = {
        "Code": 0,
        "Message": "Success",
        "RequestId": str(uuid.uuid4()),
        "Data": data
    }
    return jsonify(post_data)


# ocr解析
def ocrProcess(imgPath, language):
    if language == "write":
        result = tesseract.ocr(imgPath)
        resMapList = []
        for line in result:
            resMap = {
                "Coordinate": {
                    "UpperLeft": 0,
                    "UpperRight": 0,
                    "LowerRight": 0,
                    "LowerLeft": 0
                },
                "Words": line["text"],
                "Score": 0
            }
            resMapList.append(resMap)
        return resMapList
    else:
        pass


import sys
from paddleocr.tools.infer.utility import base64_to_cv2
from time import strftime,localtime
import random
import cv2
import numpy as np
import os

@app.route("/ocr/server", methods=['POST', 'GET'])
def ocr_server():
    try:
        # params = request.get_json()
        content = request.form

        images = content['image']
        language = content['language']
        images_decode = [base64_to_cv2(images)]
        img_decode = images_decode[0]
       
        #print(type(img_decode))
        if(not os.path.exists("./temp")):
            os.makedirs("./temp")

        t = strftime("%Y_%m_%d_%H_%M_%S", localtime())
        imgPath = './temp/' + t + '_' + str(random.randint(1000,9999)) +'.jpg'
        cv2.imwrite(imgPath, img_decode)
        #进行OCR识别
        res = ocrProcess(imgPath,language)
        os.unlink(imgPath)
        return jsonSuccess(res)

    except Exception as err:
        print_exc()
        return jsonFail(err)

if __name__ == "__main__" :
    app.run(debug=False, host="0.0.0.0", port=6666, threaded=False)