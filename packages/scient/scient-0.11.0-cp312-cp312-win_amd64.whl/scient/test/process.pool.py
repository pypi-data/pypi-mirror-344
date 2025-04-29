# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 19:30:35 2024

@author: ThinkPad
"""
import os
dirpath=os.path.dirname(__file__)
import sys
sys.path.append(os.path.join(dirpath,'../..'))

from scient import process
import time
from multiprocessing import cpu_count
import pandas
#%%
if __name__=='__main__':
    data=list(range(2))
    t=time.time()
    result=process.pool(process.as_numeric,data,n_worker=cpu_count())
    print(time.time()-t)
    
    t=time.time()
    result=process.pool(process.as_numeric,data,n_worker=2)
    print(time.time()-t)
    
    t=time.time()
    result=process.pool(process.as_numeric,data,n_worker=1)
    print(time.time()-t)
    
    data=pandas.Series(range(10000))
    t=time.time()
    result=process.pool(process.as_numeric,data,n_worker=cpu_count())
    print(time.time()-t)
    
    data=pandas.Series(range(10000))
    data=pandas.concat((data,data),axis=1)
    t=time.time()
    result=process.pool(process.as_numeric,data,n_worker=cpu_count())
    print(time.time()-t)
    
    t=time.time()
    result=process.pool(process.as_numeric,data.T,n_worker=cpu_count())
    print(time.time()-t)
    
    t=time.time()
    result=process.pool(process.as_numeric,data.values,n_worker=cpu_count())
    print(time.time()-t)

