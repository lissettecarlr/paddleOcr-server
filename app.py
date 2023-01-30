import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"

import paddleocr.paddleocr
from paddleocr.paddleocr import PaddleOCR
from flask import Flask, request, jsonify
from traceback import print_exc
import json
import uuid

# 2.3版本可用
paddleocr.paddleocr.BASE_DIR = "./"

japOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="japan", enable_mkldnn=True)
engOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="en", enable_mkldnn=True)
korOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="korean", enable_mkldnn=True)
chOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="ch", enable_mkldnn=True)

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


def ocrResultSort(ocr_result):
    ocr_result.sort(key=lambda x: x[0][0][1])

    # 二次根据纵坐标数值分组（分行）
    all_group = []
    new_group = []
    flag = ocr_result[0][0][0][1]
    pram = max([int((i[0][3][1] - i[0][0][1]) / 2) for i in ocr_result])

    for sn, i in enumerate(ocr_result):
        if abs(flag - i[0][0][1]) <= pram:
            new_group.append(i)
        else:
            all_group.append(new_group)
            flag = i[0][0][1]
            new_group = [i]
    all_group.append(new_group)

    # 单行内部按左上点横坐标排序
    all_group = [sorted(i, key=lambda x: x[0][0][0]) for i in all_group]
    # 去除分组，归一为大列表
    all_group = [ii for i in all_group for ii in i]
    # 列表输出为排序后txt
    all_group = [ii for ii in all_group]

    return all_group


# ocr解析
def ocrProcess(imgPath, language):
    print("language = {}".format(language))
    if language in ["JAP","japan"]:
        result = japOcr.ocr(imgPath, cls=False)
    elif language in ["ENG","en"]:
        result = engOcr.ocr(imgPath, cls=False)
    elif language in ["KOR","korean"]:
        result = korOcr.ocr(imgPath, cls=False)
    elif language in ["CH","ch"]:
        result = chOcr.ocr(imgPath, cls=False)
    else:#其他未知的都按照日语识别
        result = japOcr.ocr(imgPath, cls=False)
        
    try:
        result = ocrResultSort(result)
    except Exception:
        pass

    resMapList = []
    for line in result:
        try:
            print(line[1][0])
        except Exception:
            pass
        resMap = {
            "Coordinate": {
                "UpperLeft": line[0][0],
                "UpperRight": line[0][1],
                "LowerRight": line[0][2],
                "LowerLeft": line[0][3]
            },
            "Words": line[1][0],
            "Score": float(line[1][1])
        }
        resMapList.append(resMap)
    #print()

    return resMapList


import sys
# 接收请求
@app.route("/ocr/api", methods=["POST"])
def getPost():
    try:
        post_data = request.get_data()
        post_data = json.loads(post_data.decode("utf-8"))

        languageList = ["JAP", "ENG", "KOR", "RU"]
        if post_data["Language"] not in languageList:
            return jsonFail("Language {} doesn't exist".format(post_data["Language"]))

        print('imgPath:{}'.format(post_data["ImagePath"]) , file=sys.stderr)
        
        res = ocrProcess(post_data["ImagePath"], post_data["Language"])
        return jsonSuccess(res)

    except Exception as err:
        print_exc()
        return jsonFail(err)


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