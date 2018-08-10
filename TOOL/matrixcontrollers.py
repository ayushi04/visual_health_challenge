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

@mod_matrixcontrollers.route('/image',methods=['POST'])
def image():
	return json.dumps({'output':str(123),'subspace':str("123")})