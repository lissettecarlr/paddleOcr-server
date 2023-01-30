import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"

import paddleocr.paddleocr
from paddleocr.paddleocr import PaddleOCR

# 2.3版本可用
paddleocr.paddleocr.BASE_DIR = "./"

# japOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="japan", enable_mkldnn=True)
# engOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="en", enable_mkldnn=True)
# korOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="korean", enable_mkldnn=True)
# chOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="ch", enable_mkldnn=True)

class localOcr():
    def __init__(self, language= "en"):
        self.ocrHander = PaddleOCR(use_angle_cls=False, use_gpu=False, lang=language, enable_mkldnn=True)
    def ocr(self,imgPath):
        result = self.ocrHander.ocr(imgPath, cls=False)
        result= ocrResultSort(result)
        
        resMapList = []
        for line in result:
            # try:
            #     print(line[1][0])
            # except Exception:
            #     pass
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
            
        return resMapList


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




if __name__ == "__main__" :
    test = localOcr()
    re = test.ocr("D:\\code\\mygit\\PaddleOCR\\test.png")
    print(re)