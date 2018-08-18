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
import heidicontroller_helper as hch

from mod_matrix import generateCustomMatrix as gcm
from mod_matrix import region_label as rg
from mod_matrix import image_module as hd
from mod_matrix import orderPoints as op

from bokeh.resources import CDN
from bokeh.embed import file_html

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

@mod_matrixcontrollers.route('/data_filter',methods=['POST','GET'])
def data_filter():
    print('-----data_filter------')
    if request.method == 'POST':
        try:
            datasetPath=request.form['datasetPath']
            #user = User(request.form['name'], request.form['phone'], generate_password_hash(request.form['password'], method='sha256'), request.form['email'])
            print(datasetPath)
            gender=request.form.getlist('gender')
            los=request.form.getlist('los')
            age=request.form.getlist('age')
            icd9=request.form.getlist('icd9');
            print('gender: %s, los : %s, age : %s, icd9 category code : %s' %(gender,los,age,icd9))
            x=pd.read_csv(filepath_or_buffer=datasetPath, sep=',',index_col='id', parse_dates=True)
            print(x.shape)
            if 'ALL' not in gender:
                x=x[x.GENDER.isin(gender)]
            if 'ALL' not in los:
                x=x[x.LOS.isin(los)]
            #if 'ALL' not in age:
            #    x=x[x.AGE.isin(age)]
            if 'ALL' not in icd9:
                x=x[x.ICD9_CATEGORY.isin(icd9)]
            print(x.shape)
            filename='filteredData.csv'
            file_uploads_path = os.path.join(config.UPLOADS_DIR, filename)
            x.to_csv(file_uploads_path, sep=',',index=True)
            datasetPath = 'static/uploads/' + filename
            #db.session.add(user)
            #db.session.commit()
            #GENERATING META-INFORMATION OF DATA
            plot=hch.getMetaInfo(inputData)
            #html=file_html(plot,CDN,"my plot")
            return render_template('data_analysis.html',title='visual tool',datasetPath=datasetPath, user=current_user)
            return "123"
            #return redirect(url_for('matrixcontrollers.image'))
        except Exception as e:
            print(e)
            flash('Wrong inputs, please check your input and try again.')
            return render_template('data_filter.html', user=current_user, datasetPath='static/uploads/V3_ICU_INPUT_NAME_PATIENT_ICD9_less.csv')


@mod_matrixcontrollers.route('/image',methods=['POST','GET'])
def image():
    print('----matrixcontrollers: image---')
    try:
        datasetPath=request.args.get('datasetPath')
        equations=request.args.get('equations')
        equations=equations.split(':')
        print('INPUT PARAMS : datasetPath: %s, equations: %s' %(datasetPath,equations))
        inputData = pd.read_csv(filepath_or_buffer=datasetPath,sep=',',index_col='id', parse_dates=True)
        #print(inputData.dtypes)
        
        #FILTEREDDATA
        order_dim=['classLabel']
        datelist=['DOB','DOD','DOD_HOSP','DOD_SSN']
        for c in datelist:
            inputData[c]=pd.to_datetime(inputData[c], errors='ignore')
        for eq in equations:
            t=gcm.mysplit(eq)
            #print(t)
            for i in t:
                if(i in inputData.columns and i not in order_dim and i not in datelist and i !='ICD9_CATEGORY' and i!='INPUTS'):
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

        print('----succesfully ordered points----')
        #CALL CODE TO GET CUSTOM IMAGE FROM DATASET AND BIT VECTOR 
        c= gcm.generateCustomMatrix()
        c.resetBitList()
        for eq in equations:
            c.appendToBitList([eq])
        print("shape of inputData to the matrix:", inputData.shape)
        matrix,bs = c.generateCustomHeidiMatrix(inputData)
        print("shape of matrix generated:",matrix.shape)
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
    except Exception as e:
        print(e)
        flash(e)
        datasetName=request.args.get('datasetPath')
        return render_template('data_analysis.html',user=current_user,datasetPath=datasetPath)
