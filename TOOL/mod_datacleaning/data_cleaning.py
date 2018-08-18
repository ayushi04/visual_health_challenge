import pandas as pd
import numpy as np
import datetime

def fix_missing(file, fix_option):
    # file.rename(columns=lambda x: x.strip(), inplace=True)
    if fix_option == 'skip':
        print (fix_option)
        file.dropna(axis=0,inplace=True)
    elif fix_option == 'mean':
        print (fix_option)
        file.dropna(axis=0, inplace=True)
        file.fillna(file.mean(axis=1), axis=0, inplace=True)
    elif fix_option == 'median':
        print (fix_option)
        file.dropna(axis=0, inplace=True)
        file.fillna(file.median(axis=1), axis=0, inplace=True)
    elif fix_option == 'max frequent':
        print (fix_option)
        file.dropna(axis=0, inplace=True)
        file.fillna(file.mode(axis=0), axis=0, inplace=True)
    elif fix_option == 'max':
        print (fix_option)
        file.dropna(axis=0, inplace=True)
        file.fillna(file.max(axis=0), axis=0, inplace=True)
    elif fix_option == 'min':
        print (fix_option)
        file.dropna(axis=0, inplace=True)
        file.fillna(file.min(axis=0), axis=0, inplace=True)
    return file


def clean(file_clean):
    #file_clean.apply(lambda x: x.apply(lambda y: y.strip() if type(y) == type('') else y), axis=0)
    #pattern = r'[\W+a-zA-Z]'
    #file_clean.replace(pattern, value='', regex=True, inplace=True)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    newdf = file_clean.select_dtypes(include=numerics)  
    for c in file_clean.columns:
        if c=='id' : newdf['id']=file_clean['id']
        if not c in list(newdf.columns):
            #print('ccc',c,file_clean[c].astype('category'))
            newdf[c]=file_clean[c].astype('category')
            newdf[[c]]=newdf[[c]].apply(lambda x:x.cat.codes)   

    return newdf

def handleDate(file_clean,datelist):
    newdf=file_clean
    for c in datelist:
        print('--',c)
        newdf[c]=newdf[c].replace('0',pd.NaT)
        newdf[c] = pd.to_datetime(newdf[c], errors='ignore')
        #newdf[c].dtype=datetime.datetime
    #print(newdf['DOD_HOSP'])
    #newdf=newdf.infer_objects()
    #print(list(newdf.dtypes))
    #newdf.dtypes=[int,int,int,float,int,str,str,datetime.datetime,datetime.datetime,datetime.datetime,str,int]
    #for c in datelist:
    #    if(datelist)
    return newdf

def id_classLabel_check(file):
    if 'id' not in file.columns:
        print("'id' not present in input data")
        return "Please add a unique column identifier labelled with column head 'id'!!"
    if 'classLabel' not in file.columns:
        return "Please add a unique cluster identifier labelled with column head 'classLabel'!!"
    if file['id'].isnull().any():
        return "Missing values are there is 'id' column!!"
    if file['classLabel'].isnull().any():
        return "Missing values are there is 'classLabel' column!!"
    if not file['id'].is_unique:
        return "'id' column values are not unique, please assign a unique value to each identifier!!"
    return True