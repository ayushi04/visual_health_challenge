from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
import os
import pandas as pd
import config
from mod_datacleaning import data_cleaning

from mod_matrix import generateCustomMatrix as gcm
from mod_matrix import region_label as rg
from mod_matrix import image_module as hd
from mod_matrix import orderPoints as op

import linecache
import sys
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    return ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

mod_matrixcontrollers = Blueprint('matrixcontrollers', __name__)

@mod_matrixcontrollers.route('/image',methods=['POST','GET'])
def image():
    #print('----matrixcontrollers: image---')
    #try:
        datasetPath=request.args.get('datasetPath')
        equations=request.args.get('equations')
        equations=equations.split(',')
        print('INPUT PARAMS : datasetPath: %s, equations: %s' %(datasetPath,equations))
        inputData = pd.read_csv(filepath_or_buffer=datasetPath,sep=',',index_col='id')
        

        #FILTEREDDATA
        order_dim=['classLabel']
        for eq in equations:
            t=gcm.mysplit(eq)
            for i in t:
                if(i in inputData.columns and i not in order_dim):
                    order_dim.append(i)
        print('------order_dim-----',order_dim)
        filtered_data = inputData.loc[:,order_dim]
        filtered_data['classLabel_orig']=filtered_data['classLabel'].values
        #ORDER POINTS
        # IF ORDERDIM LENGTH =1 THEN ORDERING BY SORTED ORDER ELSE SOME OTHER ORDERING SCHEMA
        if len(order_dim)==2:
            param={}
            param['columns']=list(filtered_data.columns[:-1])
            param['order']=[True for i in param['columns']]
            sorted_data=op.sortbasedOnclassLabel(filtered_data,'dimension',param)
            # REINDEXING THE INPUT DATA (TO BE USED LATER)
            sorting_order=sorted_data.index
            inputData=inputData.reindex(sorting_order)
        else:
            print('mst ordering')
            param={}
            sorted_data=op.sortbasedOnclassLabel(filtered_data,'knn_bfs',param)#'mst_distance' #connected_distance
            #sorted_data=op.sortbasedOnclassLabel(filtered_data,'euclidian_distance',param)
            sorting_order=sorted_data.index
            inputData=inputData.reindex(sorting_order)


        #CALL CODE TO GET CUSTOM IMAGE FROM DATASET AND BIT VECTOR 
        c= gcm.generateCustomMatrix()
        c.resetBitList()
        for eq in equations:
            c.appendToBitList([eq])
        print(inputData.shape)
        matrix,bs = c.generateCustomHeidiMatrix(inputData)
        print(matrix.shape)
        print('----matrix generated ---')
        #lbl=rg.regionLabelling_8(matrix)
        #print('---region labelling done ---')
        #tmp=pd.DataFrame(lbl)
        tmp=pd.DataFrame(matrix)
        output='static/output'
        img,dict1=hd.generateHeidiMatrixResults_noorder_helper(matrix,bs,output,inputData,'legend_heidi')
        print('--generated image ---')
        #SAVE IMAGE IN DATABASE
        #SAVE DATASET IN DATABASE (OPTIONAL)
        #SAVE IMAGE IN OUTPUT DIRECTORY
        return json.dumps({'output':str(123),'subspace':str("123")})
    #except Exception as e:
    #    print(e)
    #    flash(e)
    #    datasetName=request.args.get('datasetPath')
    #    return render_template('data_analysis.html',user=current_user,datasetPath=datasetPath)
