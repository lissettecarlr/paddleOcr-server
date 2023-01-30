#不通过请求而是直接下载模型本地识别

import pytesseract
from PIL import Image
from loguru import logger

class tesseractOcr:
    def __init__(self):
        self.config = r'--dpi 300 --psm 6'
        self.lang = 'mnist'

    def ocr(self,imgPath):
        res = pytesseract.image_to_string(Image.open(imgPath), lang=self.lang ,config=self.config)
        logger.info(res)
        resList = res.splitlines()
        logger.info(resList)
        rtList = []
        for line in resList:
            lineJson = {
                "text":line
            }
            rtList.append(lineJson)
        return rtList


# 输出 [{'text': '11'}, {'text': '1'}]
if __name__ == '__main__':
    test = tesseractOcr()
    re = test.ocr("test.png")
    print(re)