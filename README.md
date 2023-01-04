# paddleOcr-server
基于paddleOcr的服务端

## 使用
首先还是安装paddle环境
```
conda create -n paddle python=3.10 
conda install paddlepaddle==2.4.1 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/
pip install --upgrade paddlehub -i https://pypi.tuna.tsinghua.edu.cn/simple
```
关于paddleOcr可以参考之前的[博文](https://blog.kala.love/posts/9eb77f73/)

然后执行命令：
```
python app.py
```
在显示 OCR 服务已启动 后则新开个控制台进入test文件夹执行
```
python .\post.py 
```
会对其发送识别请求来测试服务有没有啥问题


## 模型
[模型地址](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md)


在运行后会自动下载，模型的保存位置在此工程目录下的whl文件夹，以下是会自动下载的模型，如果需要修改则在paddleocr.py文件中找到MODEL_URLS参数，修改其中的下载链接即可

### 检测类
* Multilingual_PP-OCRv3_det_infer  原始超轻量模型，支持多语言检测
* en_PP-OCRv3_det_infer 原始超轻量模型，支持英文、数字检测
* ch_PP-OCRv3_det_infer 简体中文检测

### 识别类
* japan_PP-OCRv3_rec_infer 日文识别
* korean_PP-OCRv3_rec_infer 韩语识别
* ch_PP-OCRv3_rec_infer 简体中文识别
* en_PP-OCRv3_rec_infer 原始超轻量模型，支持英文、数字识别

### 角度分类
* ch_ppocr_mobile_v2.0_cls_infer  原始分类器模型，对检测到的文本行文字角度分类

### 更改中文检测和识别模型
在模型地址中能够找到ch_ppocr_server_v2.0_rec和ch_ppocr_server_v2.0_det两个模型，比起OCRv3，他们有更好的检测识别率，但是意味着耗时更长。如果对准确性有更高要求则可以进行模型的更换
paddleocr.py文件中MODEL_URLS参数中'det'->'ch'的url改为
```
https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_det_infer.tar
```
'rec'->‘ch’的url改为
```
https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_server_v2.0_rec_infer.tar
```





