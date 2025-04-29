# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:30:32 2024

@author: ThinkPad
"""
import os
data_path=os.path.dirname(__file__)+'/data'
import sys
sys.path.append(os.path.join(data_path,'../../..'))

import numpy
import pandas
from PIL import Image
from scient.image import feature,threshold,edge
from scient.algorithm import entropy
from tqdm import tqdm

images=[os.path.join(data_path,i) for i in os.listdir(data_path) if i.endswith('.bmp') or i.endswith('.png') or i.endswith('.JPEG') or i.endswith('.jpg')]

images=[Image.open(i) for i in images]
images=[i for i in images if i.mode in ('RGBA','RGB')]

features=[]
for image in tqdm(images):
    features.append({'filename':image.filename})
    
    #整体属性
        #图像分辨率
    features[-1].update({'height':numpy.array(image).shape[0],
                         'width':numpy.array(image).shape[1],
                         'channel':numpy.array(image).shape[2]})
        #图像信息熵
    features[-1].update({'entropy':entropy.discrete_prob(numpy.array(image).flatten())})
    #brisque
    features[-1].update(zip(['mscn','gdd',
                             'aggd_α1','aggd_η1','aggd_σl1','aggd_σr1',
                             'aggd_α2','aggd_η2','aggd_σl2','aggd_σr2',
                             'aggd_α3','aggd_η3','aggd_σl3','aggd_σr3',
                             'aggd_α4','aggd_η4','aggd_σl4','aggd_σr4'],
                             feature.brisque(numpy.array(image.convert('L')))))
    #清晰程度
        #平均梯度
    features[-1].update({'mean_gradient':feature.mean_grad(numpy.array(image.convert('L')))})
        #基于累积概率的清晰度
    features[-1].update({'cumprob_blur':feature.cumprob(numpy.array(image.convert('L')))})
    #曝光质量
        #平均亮度
    features[-1].update({'mean_bright':numpy.array(image.convert('L')).mean()})
        #基于灰度分位数的曝光度
    features[-1].update(zip(['gray_quantile_bright','gray_quantile_dark'],
                            feature.gray_quantile_expose(numpy.array(image.convert('L')))))
        #基于分块明度的曝光度
    features[-1].update(zip(['block_value_bright','block_value_dark'],
                            feature.block_value_expose(numpy.array(image))))
    #倾斜畸变
        #霍夫线变换
    image_=numpy.array(image.convert('L')).copy()
    thres=threshold.otsu(image_)
    image_[image_>thres]=255
    image_[image_<=thres]=0
    edge_image=edge.canny(image_).astype(numpy.uint8)
    lines=edge.houghline(edge_image, threshold=150)
    if len(lines)>0:
        angle=sorted([(r,min(abs(t-0),abs(t-numpy.pi/2),abs(numpy.pi-t))) for r,t in lines],key=lambda x:x[1])[0][1]
    else:
        angle=0
    features[-1].update({'angle':angle})
    
features=pandas.DataFrame(features)
print(features)

