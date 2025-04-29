# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 18:03:39 2024

@author: ThinkPad
"""

import os
data_path=os.path.dirname(__file__)+'/data'
import sys
sys.path.append(os.path.join(data_path,'../../..'))

from scient.image import dedup
from PIL import Image
import numpy

if __name__=='__main__':
    images=[os.path.join(data_path,i) for i in os.listdir(data_path) if i.endswith('.bmp') or i.endswith('.png') or i.endswith('.JPEG') or i.endswith('.jpg')]
    ref_image=data_path+'/I10.BMP'

    #encode
    # dedup_task=dedup.Hash()
    dedup_task=dedup.Hash(n_worker=6)
    print('encode',dedup_task.encode(numpy.array(Image.open(ref_image))))
    print('encode file',dedup_task.encode_file(ref_image))
    print('encode files',dedup_task.encode_files(images))
    print('encode files not dict',dedup_task.encode_files(images,return_dict=False))
    print('encode folder',dedup_task.encode_folder(data_path))
    
    dedup_task=dedup.Hash(hash_hex=True)
    print('encode folder hex',dedup_task.encode_folder(data_path))
    print('encode zipfile hex',dedup_task.encode_archive(data_path+'/imagewoof_train.zip',mode='zipfile'))
    print('encode tarfile hex',dedup_task.encode_archive(data_path+'/imagewoof_val.tar.gz',mode='tarfile'))
    
    #find_dup
    print('find_dup_from_map',dedup_task.find_dup_from_map(dedup_task.encode_file(ref_image),dedup_task.encode_folder(data_path)))
    print('find_dup_in_map',dedup_task.find_dup_in_map(dedup_task.encode_files(images)))
    score={i:numpy.random.randint(0,10) for i in images}
    print('find_dup_in_map score',dedup_task.find_dup_in_map(dedup_task.encode_folder(data_path)))
    print('find_dup_from_files',dedup_task.find_dup_from_files(ref_image,images))
    print('find_dup_in_files',dedup_task.find_dup_in_files(images))
    print('find_dup_in_files score',score,dedup_task.find_dup_in_files(images,score=score))
    print('find_dup_from_folder',dedup_task.find_dup_from_folder(ref_image,data_path))
    print('find_dup_in_folder',dedup_task.find_dup_in_folder(data_path))
    score={os.path.basename(k):v for k,v in score.items()}
    print('find_dup_in_folder score',dedup_task.find_dup_in_folder(data_path,score=score))
    print('find_dup_from_archive zipfile',dedup_task.find_dup_from_archive(data_path+'/ILSVRC2012_val_00020553.JPEG',data_path+'/imagewoof_train.zip',mode='zipfile'))
    print('find_dup_in_archive zipfile',dedup_task.find_dup_in_archive(data_path+'/imagewoof_train.zip',mode='zipfile'))
    import zipfile
    zf=zipfile.ZipFile(data_path+'/imagewoof_train.zip')
    score={i.filename:numpy.random.randint(0,10) for i in zf.filelist if not i.is_dir()}
    print('find_dup_in_archive zipfile score',dedup_task.find_dup_in_archive(data_path+'/imagewoof_train.zip',score=score,mode='zipfile'))
    print('find_dup_from_archive tarfile',dedup_task.find_dup_from_archive(data_path+'/ILSVRC2012_val_00010420.JPEG',data_path+'/imagewoof_val.tar.gz',mode='tarfile'))
    print('find_dup_in_archive tarfile',dedup_task.find_dup_in_archive(data_path+'/imagewoof_val.tar.gz',mode='tarfile'))
    
    dedup_task=dedup.Hash(threshold=5)
    print('find_dup_in_files',dedup_task.find_dup_in_files(images))
    dedup_task=dedup.Hash(hash_size=128,hash_hex=True)
    print('encode file',dedup_task.encode_file(ref_image))
    print('find_dup_in_files',dedup_task.find_dup_in_files(images))
    
    
    # hash_func
    # dist_func
    # process_func
    # scale
    # errors
    # suffix
    # n_worker


