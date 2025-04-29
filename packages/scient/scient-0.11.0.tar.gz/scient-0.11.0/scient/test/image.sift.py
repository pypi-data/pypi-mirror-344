# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 19:07:21 2024

@author: ThinkPad
"""

import numpy
from matplotlib import pyplot as plt
from PIL import Image
import time
import cv2
from scient.algorithm import similar
from scient.image import sift

MIN_MATCH_COUNT = 10

img1=Image.open('data/box.png').convert('L')
img2=Image.open('data/box_in_scene.png').convert('L')
img1=numpy.array(img1)
img2=numpy.array(img2)

sift_task=sift.SIFT()

# Compute SIFT keypoints and descriptors
t=time.time()
kp1, des1 = sift_task.detect(img1,n_point=100)
print('--',time.time()-t)
t=time.time()
kp2, des2 = sift_task.detect(img2,n_point=100)
print('--',time.time()-t)

#关键点匹配相似度
bf = cv2.BFMatcher()
#记录图1和图2的匹配的关键点
matches1 = bf.knnMatch(des1,des2,k=2)
top_results1 = []
for m,n in matches1:
    if m.distance < 0.7 * n.distance:
        top_results1.append(m)
#记录图2和图1匹配的关键点
matches2 = bf.knnMatch(des2,des1,k=2)
top_results2 = []
for m,n in matches2:
    if m.distance < 0.7 * n.distance:
        top_results2.append(m)
print('关键点匹配相似度_:',2*len(top_results1)/len(matches1)*len(matches2)/len(matches2)/(len(top_results1)/len(matches1)+len(matches2)/len(matches2)))
#从匹配的关键点中选择出有效的匹配
#确保匹配的关键点信息在图1和图2以及图2和图1是一致的
top_results = []
for m1 in top_results1:
    m1_query_idx = m1.queryIdx
    m1_train_idx = m1.trainIdx

    for m2 in top_results2:
        m2_query_idx = m2.queryIdx
        m2_train_idx = m2.trainIdx

        if m1_query_idx == m2_train_idx and m1_train_idx == m2_query_idx:
            top_results.append(m1)
            
#计算图像之间的相似度
#通过计算两张图片之间的匹配的关键点的个数来计算相似度
image_sim = len(top_results) / min(len(kp1),len(kp2))
print('关键点匹配相似度:',image_sim,'关键点匹配数量',len(top_results))

#描述向量相似度
vector1=sorted(zip(kp1,des1),key=lambda x:-x[0]['func_value'])
vector2=sorted(zip(kp2,des2),key=lambda x:-x[0]['func_value'])
vector1=[d for k,d in vector1]
vector2=[d for k,d in vector2]
vector1=numpy.concatenate(vector1)
vector2=numpy.concatenate(vector2)
vector1=vector1[:128*100]
vector2=vector2[:128*100]
if len(vector1)<128*100:
    vector1=numpy.concatenate(vector1,numpy.zeros(128*100 - vector1.size))
if len(vector2)<128*100:
    vector2=numpy.concatenate(vector2,numpy.zeros(128*100 - vector2.size))
print('描述向量相似度:',similar.cosine(vector1,vector2))

#目标检索
# Initialize and use FLANN
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
# Lowe's ratio test
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)
if len(good) > MIN_MATCH_COUNT:
    # Estimate homography between template and scene
    src_pts = numpy.float32([ (kp1[m.queryIdx]['x'],kp1[m.queryIdx]['y']) for m in good]).reshape(-1, 1, 2)
    dst_pts = numpy.float32([ (kp2[m.trainIdx]['x'],kp2[m.trainIdx]['y']) for m in good]).reshape(-1, 1, 2)

    M = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)[0]

    # Draw detected template in scene image
    h, w = img1.shape
    pts = numpy.float32([[0, 0],
                      [0, h - 1],
                      [w - 1, h - 1],
                      [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    img2 = cv2.polylines(img2, [numpy.int32(dst)], True, 255, 3, cv2.LINE_AA)

    h1, w1 = img1.shape
    h2, w2 = img2.shape
    nWidth = w1 + w2
    nHeight = max(h1, h2)
    hdif = int((h2 - h1) / 2)
    newimg = numpy.zeros((nHeight, nWidth, 3), numpy.uint8)

    for i in range(3):
        newimg[hdif:hdif + h1, :w1, i] = img1
        newimg[:h2, w1:w1 + w2, i] = img2

    # Draw SIFT keypoint matches
    rest=[]
    for m in good:
        
        pt1 = (int(kp1[m.queryIdx]['x']), int(kp1[m.queryIdx]['y'] + hdif))
        pt2 = (int(kp2[m.trainIdx]['x'] + w1), int(kp2[m.trainIdx]['y']))
        cv2.line(newimg, pt1, pt2, (255, 0, 0))

    plt.imshow(newimg)
    plt.show()
else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
