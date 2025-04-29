# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 10:17:22 2024

@author: ThinkPad
"""
import os
data_path=os.path.dirname(__file__)+'/data'
import sys
sys.path.append(os.path.join(data_path,'../../..'))

from scient.language import tokenize
import pandas

corpus=pandas.read_excel(data_path+'/text_pair_corpus.xlsx')
corpus=pandas.concat((corpus['input'],corpus['label'])).drop_duplicates().tolist()
corpus=[i.strip() for i in corpus if len(i.strip())>0]

sp=tokenize.SentPiece()
sp.fit(corpus,vocab_size=3000,batch_size=100,n_iter=10)

import pickle
pickle.dump(sp,open('spmodel','wb'))

print('sp',sp.split(corpus[0]))
print('sp',sp.encode(corpus[0]))
print('sp',sp.decode(sp.encode(corpus[0])))

sp1=tokenize.SentPiece(vocab=sp.token2id)
print('sp1',sp1.encode(corpus[0]))
print('sp1',sp1.decode(sp1.encode(corpus[0])))

sp2=pickle.load(open('spmodel','rb'))
print('sp2',sp2.encode(corpus[0]))
print('sp2',sp2.decode(sp.encode(corpus[0])))

sp3=tokenize.SentPiece('spmodel')
print('sp3',sp3.encode(corpus[0]))
print('sp3',sp3.decode(sp1.encode(corpus[0])))


