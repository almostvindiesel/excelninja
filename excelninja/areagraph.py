#!/usr/bin/env python
# -*- coding: utf-8 -*-
print "Loading " + __file__

import os
import datetime
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

from sqlalchemy import UniqueConstraint, distinct, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from flaskext.mysql import MySQL
import MySQLdb

# --------------------------------------------------------------------------------
# Dashboard Home


@app.route('/twitter', methods=['GET'])
def show_areagraph():
    return render_template('areagraph.html')
