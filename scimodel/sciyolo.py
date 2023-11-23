import torch 
from ultralytics import YOLO
from scimodel.SCImain.model import Finetunemodel
from PIL import Image
import numpy as np
import cv2
from torch.autograd import Variable
import torchvision.transforms as transforms
def save_images(tensor):
        image_numpy = tensor[0].cpu().detach().float().numpy()
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)))
        im = Image.fromarray(np.clip(image_numpy * 255.0, 0, 255.0).astype('uint8'))
        return im
class SCIYOLO(torch.nn.Module):
    def __init__(self,yoloweight,sciweight):
        super(SCIYOLO,self).__init__()
        self.sci = Finetunemodel(sciweight)
        model = YOLO(r".\ultralytics\models\V8\yolov8s.yaml")
        model = YOLO(yoloweight)
        self.yolov8=model
        self.conf=0.7
    def forward(self,x,conf=0.7):
        transform_list = []
        transform_list += [transforms.ToTensor()]
        transform = transforms.Compose(transform_list)
        im = Image.fromarray(x)
        img_norm = transform(im).numpy()
        img_norm = np.transpose(img_norm, (1, 2, 0))
        low = np.asarray(img_norm, dtype=np.float32)
        low = np.expand_dims(low.transpose((2,0,1)),0)
        img_tensor=torch.from_numpy(low)
        i, r = self.sci(img_tensor)
        img = save_images(r)
        p = self.yolov8.predict(x,conf=conf)
        return p