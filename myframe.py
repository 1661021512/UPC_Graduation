# 检测的接口函数

import cv2
import time
import random
from scimodel.sciyolo import SCIYOLO

weights = r'weights/EXdark.pt'
sciweight=r'scimodel\SCImain\weights\easy.pt'
opt_device = ''  # device = 'cpu' or '0' or '0,1,2,3'
imgsz = 640

# Load model
model = SCIYOLO(yoloweight=weights,sciweight=sciweight)
names = model.yolov8.module.names if hasattr(model, 'module') else model.yolov8.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
# cap = cv2.VideoCapture(0)

def frametest(frame,conf):
    # frame为帧输入
    # 定义返回变量
    ret = []
    labellist = []

    # 计时开始，用于计算fps
    tstart = time.time()

    pred = model(frame,conf=conf)
    labellist=[]
    for result in pred:
        boxes = result.boxes  # Boxes object for bbox outputs
        for box in boxes:
            label = f'{names[int(box.cls)]}'
            labellist.append(label)
    frame=pred[0].plot()

    ret.append(labellist)
    # 计时结束
    tend = time.time()
    # 计算fps
    fps=1/(tend-tstart)
    fps = "%.2f fps" % fps
    # 在图片的左上角标出Fps
    # cv2.putText(frame,fps,(10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    # 返回ret 和 frame
    return ret,frame,fps