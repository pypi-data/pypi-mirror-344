# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:09:19 2024

@author: ThinkPad
"""
import os
data_path=os.path.dirname(__file__)
import sys
sys.path.append(os.path.join(data_path,'../../..'))

import pandas
from scient.cluster import fourstep

#3d
x=pandas.read_csv(data_path+'/3d_guassian_mix.csv')
clm=fourstep.FourStep(plot=True)
clm.fit(x.values)
#2d
x=pandas.read_csv(data_path+'/3d_guassian_mix.csv')
clm=fourstep.FourStep(plot=True)
clm.fit(x.values[:,:2])
#1d
x=pandas.read_csv(data_path+'/3d_guassian_mix.csv')
clm=fourstep.FourStep(plot=True)
clm.fit(x.values[:,:1])

