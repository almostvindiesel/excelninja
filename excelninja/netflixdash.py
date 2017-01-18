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

@app.route('/netflix', methods=['GET'])
def netflix():
    print "-" * 50

    filter_values = initialize_video_filter_values()
    filter_sql = initialize_video_filter_sql()

    #Set initial filter to HBO and Netflix
    filter_values['measure1'] = 'Narcos'
    filter_values['measure2'] = 'Stranger Things'


    measure1 = get_dashboard_filters(filter_values, 'measure1')
    measure2 = get_dashboard_filters(filter_values, 'measure2')

    #print "---/netflix: measure1"
    #print measure1

    #print "---//netflix: measure2"
    #print measure2

    return render_template('netflixdash.html', measure1=measure1, measure2=measure2) #, countries=countries, age_ranges=age_ranges, genders=genders)


# --------------------------------------------------------------------------------
# API Helpfer Functions

def initialize_video_filter_values():
    filter_values = dict()
    filter_values['measure1'] = ''
    filter_values['measure2'] = ''
    return filter_values


def initialize_video_filter_sql():
    filter_sql = dict()
    filter_sql['measure1'] = ''
    filter_sql['measure2'] = ''
    return filter_sql


def update_video_filter_values(filter_values): 

    
    #filter_categories = ['genders','countries','age_ranges']
    filter_categories = ['measure1','measure2']

    #print "update_videos: filter_categories: "
    #print filter_categories

    #print "update_video: filter_values: "
    #print filter_values

    #print "update_video: request.form.get(filter_category)"
    #print request.form.get('measures1')
    #print request.form


    #print "update_video: prior filter_values:  ", filter_values
    for filter_category in filter_categories:
        if request.form.get(filter_category):
            #print "form for filter_category: ", filter_category
            #print request.form.get(filter_category)
            filter_values[filter_category] = request.form.get(filter_category)
    

    #print "update_video: update filter_values: ", filter_values
    

    return filter_values


def update_video_filter_sql(filter_values, filter_sql): 

    if len(filter_values['measure1']) == 0:
        filter_sql['measure1'] = ' and 1=1'
    else:
        filter_sql['measure1'] =' and measure in (' + apply_quotes(filter_values['measure1']) + ')'
    
    if len(filter_values['measure2']) == 0:
        filter_sql['measure2'] = ' and 1=1'
    else:
        filter_sql['measure2'] =' and measure in (' + apply_quotes(filter_values['measure2']) + ')'
    """
    if len(filter_values['genders']) == 0:
        filter_sql['genders'] = ' and 1=1'
    else:
        filter_sql['genders'] =' and gender in (' + ','.join(map(apply_quotes, filter_values['genders'])) + ')'

    if len(filter_values['age_ranges']) == 0:
        filter_sql['age_ranges'] = ' and 1=1'
    else:
        filter_sql['age_ranges'] =' and age_range in (' + ','.join(map(apply_quotes, filter_values['age_ranges'])) + ')'

    if len(filter_values['countries']) == 0:
        filter_sql['countries'] = ' and 1=1'
    else:
        filter_sql['countries'] =' and country in (' + ','.join(map(apply_quotes, filter_values['countries'])) + ')'
    """
    
    #print "updated filter sql: ", filter_sql
    return filter_sql


def apply_quotes(x):
    return "'%s'" % text(x)


"""

filter_values['measure1'] = 'Netflix'
filter_values['measure2'] = 'HBO'
measure1 = get_dashboard_filters(filter_values, 'measure1')
"""



def get_dashboard_filters(filter_values, filter_name):
    if filter_name == 'measure1' or filter_name  == 'measure2':
        sql =  "select distinct measure from video_demographics"

        #print "get_dashboard_filters: filter values: "
        #print filter_values
        result = db.engine.execute(sql)

        datums  = []
        for row in result:
            datum = dict()
            if filter_values[filter_name] == row[0]:
                datum['selected'] = 'selected'
                #print "~~~ datum:"
                #print datum
            datum[filter_name] = row[0]
            #print "~~~ datum:"
            #print datum
            datums.append(datum)

        #print datums
        return datums

        

     
    


# --------------------------------------------------------------------------------
# API: Endpoints which return data results or filtering selections

@app.route('/netflix/api/country.json', methods=['GET','POST'])
def netflix_country():

    filter_values = initialize_video_filter_values()
    filter_sql    = initialize_video_filter_sql()
    
    filter_values = update_video_filter_values(filter_values)
    filter_sql    = update_video_filter_sql(filter_values, filter_sql)

    #print "--- netflix_country: filter_values: "
    #print filter_values

    sql =  "select \
              vd.country, \
              cast( sum(case when vd.measure = '%s' then vd.reach else 0 end) as signed) measure1_reach, \
              cast( sum(case when vd.measure = '%s' then vd.reach else 0 end) as signed) measure2_reach \
            from video_demographics vd \
            group by 1 \
            order by 3 desc " % (filter_values['measure1'],filter_values['measure2'])

    #print sql
    result = db.engine.execute(sql)

    data = []
    datasets = []
    countries  = []
    measure1_data  = []
    measure2_data = []
    for row in result:
        countries.append(row[0])
        measure1_data.append(row[1])
        measure2_data.append(row[2])


    measure1 = dict (
        label = 'measure1',
        data  = measure1_data,
        backgroundColor = "#066ff2"
    )
    measure2 = dict (
        label = 'measure2',
        data  = measure2_data,
        backgroundColor = "#772112"
    )
    datasets.append(measure1)
    datasets.append(measure2)

    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)

@app.route('/netflix/api/agepct.json', methods=['GET','POST'])
def netflix_age_pct():

    filter_values = initialize_video_filter_values()
    filter_sql    = initialize_video_filter_sql()

    filter_values = update_video_filter_values(filter_values)
    filter_sql    = update_video_filter_sql(filter_values, filter_sql)

    m1 = filter_values['measure1']
    m2 = filter_values['measure2']

    sql =  "select \
              num.age_range, \
              cast(round(sum(case when num.measure = '%s' then num.reach else 0 end) * 100 / \
                   max(case when den.measure = '%s' then den.reach else 0 end),0) as signed) sc_pct, \
              cast(round(sum(case when num.measure = '%s' then num.reach else 0 end) * 100 / \
                   max(case when den.measure = '%s' then den.reach else 0 end),0) as signed) ig_pct \
            from ( \
                select \
                  measure, \
                  sum(reach) reach \
                from video_demographics \
                where measure in ('%s', '%s') \
                group by 1 \
            ) den inner join ( \
                select \
                  measure, \
                  CONCAT(age_min, '-', age_max) age_range, \
                  sum(reach) reach \
                from video_demographics \
                where measure in ('%s', '%s') \
                group by 1,2 \
            ) num on num.measure = den.measure \
            group by 1 \
            order by 1 asc" % (m1, m1, m2, m2, m1, m2, m1, m2)

    result = db.engine.execute(sql)

    data = []
    datasets = []
    countries  = []
    measure1_data  = []
    measure2_data = []
    for row in result:
        countries.append(row[0])
        measure1_data.append(row[1])
        measure2_data.append(row[2])

    measure1 = dict (
        label = m1,
        data  = measure1_data,
        backgroundColor = "#066ff2"
    )
    measure2 = dict (
        label = m2,
        data  = measure2_data,
        backgroundColor = "#772112"
    )
    datasets.append(measure1)
    datasets.append(measure2)

    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)

@app.route('/netflix/api/genderpct.json', methods=['GET','POST'])
def netflix_gender_pct():
    print "netflix_gender_pct----------"

    filter_values = initialize_video_filter_values()
    filter_sql    = initialize_video_filter_sql()

    filter_values = update_video_filter_values(filter_values)
    filter_sql    = update_video_filter_sql(filter_values, filter_sql)

    measure = request.form.get('measure') 

    sql =  "select \
              num.gender, \
              cast(round(sum(case when num.measure = '%s' then num.reach else 0 end) * 100 / \
                   max(case when den.measure = '%s' then den.reach else 0 end),0) as signed) measure_pct \
            from ( \
                select \
                  measure, \
                  sum(reach) reach \
                from video_demographics \
                where measure in ('%s') \
                group by 1 \
            ) den inner join ( \
                select \
                  measure, \
                  gender, \
                  sum(reach) reach \
                from video_demographics \
                where measure in ('%s') \
                group by 1,2 \
            ) num on num.measure = den.measure \
            group by 1 \
            order by 1 asc"  % (measure, measure, measure, measure)
    result = db.engine.execute(sql)

    data = []
    datasets = []
    countries  = []
    age_data  = []
    for row in result:
        countries.append(row[0])
        age_data.append(row[1])

    backgroundColor = ['#ce3535','#2219ef']
    age = dict (
        label = measure,
        data  = age_data,
        backgroundColor = backgroundColor
    )

    datasets.append(age)
    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    print "--- gender data: "
    print data
    return jsonify(data)



