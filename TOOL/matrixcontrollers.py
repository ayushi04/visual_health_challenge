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
	print('----matrixcontrollers: image---')
	try:
		datasetName=request.args.get('datasetPath')
		equations=request.args.get('equations')
		print('INPUT PARAMS : datasetPath: %s, equations: %s' %(datasetName,equations))
		#CALL CODE TO GET CUSTOM IMAGE FROM DATASET AND BIT VECTOR 
		#SAVE IMAGE IN DATABASE
		#SAVE DATASET IN DATABASE (OPTIONAL)
		#SAVE IMAGE IN OUTPUT DIRECTORY
		return json.dumps({'output':str(123),'subspace':str("123")})
	except Exception as e:
		flash(e)
		datasetName=request.args.get('datasetPath')
		return render_template('data_analysis.html',user=current_user,datasetPath=datasetName)
