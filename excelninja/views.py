#!/usr/bin/env python
# -*- coding: utf-8 -*-
print ("Loading " + __file__)


import os
import datetime
import random
import requests
import requests.packages.urllib3
import json
import xmltodict, json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from datetime import date,timedelta
from werkzeug.utils import secure_filename
requests.packages.urllib3.disable_warnings()
import sys
from excelninja import app
from models import db
from snapinstadash import *
from netflixdash import *
from areagraph import *
from appledash import *
from api import *


# Required for correct utf8 encoding calls from heroku
reload(sys)
sys.setdefaultencoding("utf-8")
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?R#LDK'

@app.route('/ring', methods=['GET'])
def ring_dmas():
	return render_template('ringdash.html')




