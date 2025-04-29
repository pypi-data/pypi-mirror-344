# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 18:49:27 2024

@author: ThinkPad
"""
from scient.image import blend
from PIL import Image
import numpy
fore_image = Image.open('data/airplane.png')
back_image = Image.open('data/work_on_tower.jpg')

fore_image=fore_image.resize((fore_image.size[0]//2,fore_image.size[1]//2))
#fore_image比back_image大
# fore_image=fore_image.resize((fore_image.size[0]*2,fore_image.size[1]*2))

fore_image=numpy.array(fore_image.convert('RGB'))
back_image=numpy.array(back_image.convert('RGB'))

image = blend.poisson(back_image, fore_image, mode='normal', offset=(20,350))

#fore_image超出back_image
# image = poisson(back_image, fore_image, method='normal', offset=(20,550))
# image = poisson(back_image, fore_image, method='normal', offset=(20,-50))
# image = poisson(back_image, fore_image, method='normal', offset=(-50,-50))

Image.fromarray(image).show()

