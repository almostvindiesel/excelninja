#!/usr/bin/env python
# -*- coding: utf-8 -*-
print ("Loading " + __file__)

from excelninja import app
import os
import shutil

import requests
import urllib
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint, distinct, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from flaskext.mysql import MySQL
import MySQLdb


db = SQLAlchemy(app)



############################################################


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():  
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

@app.cli.command('initdb')
def initdb_command():
    """ s the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db



