# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 19:08:46 2024

@author: ThinkPad
"""
import os
data_path=os.path.dirname(__file__)+'/data'
import sys
sys.path.append(os.path.join(data_path,'../../..'))

import torch
from scient.neuralnet import resnet, fit
import torchvision.transforms as tt
from torchvision.datasets import ImageFolder

# 数据转换（归一化和数据增强）
stats = ((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
train_tfms = tt.Compose([tt.RandomCrop(160, padding=4, padding_mode='reflect'), 
                         tt.RandomHorizontalFlip(), 
                         tt.ToTensor(), 
                         tt.Normalize(*stats,inplace=True)])
valid_tfms = tt.Compose([tt.Resize([160,160]),tt.ToTensor(), tt.Normalize(*stats)])

# 创建ImageFolder对象
import zipfile
zf=zipfile.ZipFile(data_path+'/imagewoof_train.zip')
zf.extractall()
import tarfile
tf=tarfile.open(data_path+'/imagewoof_val.tar.gz')
tf.extractall()
data_train = ImageFolder('train', train_tfms)
data_eval = ImageFolder('val', valid_tfms)

# 设置批量大小
batch_size = 2

# 创建训练集和验证集的数据加载器
train_loader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, shuffle=True)
eval_loader = torch.utils.data.DataLoader(data_eval, batch_size=batch_size, shuffle=False)

#resnet50模型
model=resnet.ResNet50(n_class=3)

#%%
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=10,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% scheduler
#设置训练参数
n_iter=5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.0001, epochs=n_iter,steps_per_epoch=len(train_loader))
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=n_iter,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% perform
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def perform_func(y_hat,y):
    y_hat=torch.concat(y_hat)
    y=torch.concat(y)
    _,y_hat=y_hat.max(axis=1)
    return round((y_hat==y).sum().item()/len(y),4)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,perform_func=perform_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% grad_func
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def grad_func(x):
    torch.nn.utils.clip_grad_value_(x, 0.1)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,grad_func=grad_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% n_batch_step
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device,n_batch_step=5)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% early_stop
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
def perform_func(y_hat,y):
    y_hat=torch.concat(y_hat)
    y=torch.concat(y)
    _,y_hat=y_hat.max(axis=1)
    return round((y_hat==y).sum().item()/len(y),4)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,perform_func=perform_func,n_iter=(3,10),device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% n_batch_plot save_path
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device,n_batch_plot=5,save_path=data_path)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))

checkpoint=torch.load(data_path+'/ResNet_iter_2.ckpt')
checkpoint.keys()
checkpoint['batch_loss']
checkpoint['model_state_dict']
#%% only train
#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
loss_func=torch.nn.CrossEntropyLoss()
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,mode=('input','target'))
#%% model 输出为 loss  mode = 'inputs' mode 没有target时，不可以用perform_func
#模型
class output_loss(torch.nn.Module):
    def __init__(self):
        super(output_loss,self).__init__()

        self.model=resnet.ResNet50(n_class=3)
        self.loss_func=torch.nn.CrossEntropyLoss()

    def forward(self,x,y):
        y_hat=self.model(x)
        return self.loss_func(y_hat,y)
    
model=output_loss()

#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
model=fit.set(model,optimizer=optimizer,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode='inputs')
#%% 模型输出为多个内容 自定义loss_func
#模型
class output_multi(torch.nn.Module):
    def __init__(self):
        super(output_multi,self).__init__()

        self.model=resnet.ResNet50(n_class=3)
        self.loss_func=torch.nn.CrossEntropyLoss()

    def forward(self,x):
        y_hat=self.model(x)
        return y_hat,x
    
model=output_multi()

loss_func_=torch.nn.CrossEntropyLoss()
def loss_func(y_hat,y):
    return loss_func_(y_hat[0],y)

#设置训练参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
model=fit.set(model,optimizer=optimizer,loss_func=loss_func,n_iter=5,device=device)

#训练
model.fit(train_loader=train_loader,eval_loader=eval_loader,mode=('input','target'))
#%% mode = 'input' mode 没有target时，不可以用perform_func

#%% mode = ('inputs','target')

