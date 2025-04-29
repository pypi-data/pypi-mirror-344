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
from scient.image import friqa

images=[os.path.join(data_path,i) for i in os.listdir(data_path) if i.endswith('.bmp') or i.endswith('.png') or i.endswith('.JPEG') or i.endswith('.jpg')]
ref_image=data_path+'/I10.BMP'

ref_image=Image.open(ref_image)
images=[Image.open(i) for i in images]
images=[i for i in images if i.size == (512, 384) and i.mode=='RGB']

#计算两幅图片的峰值信噪比psnr
print('psnr:\n',
      pandas.DataFrame([friqa.psnr(numpy.array(ref_image),numpy.array(i)) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的结构相似度ssim
print('ssim:\n',
      pandas.DataFrame([friqa.ssim(numpy.array(ref_image.convert("L")),numpy.array(i.convert("L"))) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的均方误差mse
from scient.algorithm import metric
print('color mse:\n',
      pandas.DataFrame([metric.mse(numpy.array(ref_image),numpy.array(i)) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
print('gray mse:\n',
      pandas.DataFrame([metric.mse(numpy.array(ref_image.convert("L")),numpy.array(i.convert("L"))) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的余弦相似度
from scient.algorithm import similar
#如果不转float,consine计算值不对
print('cosine similar:\n',
      pandas.DataFrame([similar.cosine(numpy.array(ref_image).astype(float).flatten(),numpy.array(i).astype(float).flatten()) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的均值哈希相似度
from scient.image import hash
mhash=hash.mean(numpy.array(ref_image.convert("L")))
mhashs=[hash.mean(numpy.array(i.convert("L"))) for i in images]
print('mean hash similar:\n',
      pandas.DataFrame([similar.hamming(i,mhash) for i in mhashs],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的差值哈希相似度
dhash=hash.diff(numpy.array(ref_image.convert("L")))
dhashs=[hash.diff(numpy.array(i.convert("L"))) for i in images]
print('diff hash similar:\n',
      pandas.DataFrame([similar.hamming(i,dhash) for i in dhashs],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的感知哈希相似度
phash=hash.percept(numpy.array(ref_image.convert("L")))
phashs=[hash.percept(numpy.array(i.convert("L"))) for i in images]
print('percept hash similar:\n',
      pandas.DataFrame([similar.hamming(i,phash) for i in phashs],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的直方图相似度
print('color hist similar:\n',
      pandas.DataFrame([friqa.histsim(numpy.array(i),numpy.array(ref_image)) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
print('gray hist similar:\n',
      pandas.DataFrame([friqa.histsim(numpy.array(i.convert('L')),numpy.array(ref_image.convert('L'))) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
#计算两幅图片的互信息
from scient.algorithm import entropy
print('color mutual info:\n',
      pandas.DataFrame([entropy.mutual(numpy.array(i).flatten(),numpy.array(ref_image).flatten()) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
print('gray mutual info:\n',
      pandas.DataFrame([entropy.mutual(numpy.array(i.convert('L')).flatten(),numpy.array(ref_image.convert('L')).flatten()) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))

#计算两幅图片的归一化互信息
from scient.algorithm import entropy
print('color mutual info norm:\n',
      pandas.DataFrame([entropy.mutual_norm(numpy.array(i).flatten(),numpy.array(ref_image).flatten()) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
print('gray mutual info norm:\n',
      pandas.DataFrame([entropy.mutual_norm(numpy.array(i.convert('L')).flatten(),numpy.array(ref_image.convert('L')).flatten()) for i in images],
                       index=[os.path.basename(i.filename) for i in images],
                       columns=[os.path.basename(ref_image.filename)]))
