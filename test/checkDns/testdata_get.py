#coding=utf-8
'''
this script reads in the feature table before vectorizing, and normalize all numerical features from 0 to 1
'''
import pandas as pd
import numpy as np
from collections import Counter
from operator import itemgetter
from sklearn import svm
from sklearn import cross_validation
import pickle
from scipy.sparse import coo_matrix

model_data = pickle.load(open('/home/APT/pylib/checkDns/pki/tld_dict.pki', 'rb'))
tld_dict = dict()
tld_dict = model_data['tld_dict']

model_data = pickle.load(open('/home/APT/pylib/checkDns/pki/extremum.pki','rb'))
extremum = model_data['extremum']

def getTestData(filename,num):
    black_list = ['ip','tld']
    feat_table = pd.read_csv(filename,delimiter=',')
    feat_matrix = pd.DataFrame()
    header = list(feat_table.columns)
    count = 0
    for i in header:
        if i in black_list:
            if i == 'tld':
                for index,k in enumerate(feat_table.ix[:,i]):
                    try:
                        value=k.decode('utf-8').lower()
                        feat_matrix.ix[index,i]=tld_dict[value]
                    except Exception,ex:
                        feat_matrix.ix[index,i]=int(6387)
                        print Exception,":",ex
                #print feat_matrix.ix[186,'tld']
            else:
                feat_matrix[i]=feat_table.ix[:,i]
        else:
            line = feat_table.ix[:,i]
            mean_ = extremum[count]
            max_ = extremum[count+1]
            min_ = extremum[count+2]
            feat_matrix[i]=(line-mean_)/(max_-min_)
            count += 3
        print 'converted %s'%i
        fw_out = open('/home/APT/pylib/checkDns/txt/testdata.txt','w')
    print num
    for m in range(0,num):
        fw_out.write('0 ')
        print m
        value=feat_matrix.ix[m,'tld']
        isInThisTld = 1
        fw_out.write('%d:%d '%(value,isInThisTld))
        for colOfFeat,i in zip(range(6388,6405),feat_matrix.ix[m,2:19]):
            if i!=i:
                i = float(-1)
            fw_out.write('%d:%.2f '%(colOfFeat,i))
        fw_out.write('\n')
    fw_out.close()
    return '/home/APT/pylib/checkDns/txt/testdata.txt'
