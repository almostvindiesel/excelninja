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


@app.route('/apple', methods=['GET'])
def subscribers():

    filter_values = apple_initialize_filter_values()
    filter_sql = apple_initialize_filter_sql()

    countries = apple_get_dashboard_filters(filter_values, 'country')
    genders = apple_get_dashboard_filters(filter_values, 'gender')
    age_ranges = apple_get_dashboard_filters(filter_values, 'age_range')

    return render_template('appledash.html', countries=countries, age_ranges=age_ranges, genders=genders)


# --------------------------------------------------------------------------------
# API Helpfer Functions

def apple_initialize_filter_values():
    filter_values = dict()
    filter_values['measure'] = '';
    filter_values['genders'] = list()
    filter_values['countries'] = list()
    filter_values['age_ranges'] = list()
    return filter_values


def apple_initialize_filter_sql():
    filter_sql = dict()
    filter_sql['genders'] = ''
    filter_sql['countries'] = ''
    filter_sql['age_ranges'] = ''
    return filter_sql


def apple_update_filter_values(filter_values): 
    filter_categories = ['genders','countries','age_ranges']

    print "prior filter_values: ", filter_values

    for filter_category in filter_categories:
        if request.form.get(filter_category):
            filter_selections = json.loads(request.form.get(filter_category))
            for filter_selection in filter_selections:
                filter_values[filter_category].append(filter_selection)
    
    print "updated filter_values: ", filter_values

    return filter_values


def apple_update_filter_sql(filter_values, filter_sql): 

    if len(filter_values['genders']) == 0:
        filter_sql['genders'] = ' and 1=1'
    else:
        filter_sql['genders'] =' and gender in (' + ','.join(map(apply_quotes, filter_values['genders'])) + ')'

    if len(filter_values['age_ranges']) == 0:
        filter_sql['age_ranges'] = ' and 1=1'
    else:
        filter_sql['age_ranges'] =  "and concat(age_min,'-',age_max) in (" + ','.join(map(apply_quotes, filter_values['age_ranges'])) + ')'

    if len(filter_values['countries']) == 0:
        filter_sql['countries'] = ' and 1=1'
    else:
        filter_sql['countries'] =' and country in (' + ','.join(map(apply_quotes, filter_values['countries'])) + ')'
    
    print "updated filter sql: ", filter_sql
    return filter_sql


def apply_quotes(x):
    return "'%s'" % text(x)

def apple_get_dashboard_filters(filter_values, filter_name):
    if filter_name == 'country':
        sql =  "select distinct country from music_sizing"
    elif filter_name == 'age_range':
        sql =  "select distinct CONCAT(age_min, '-', age_max) age_range from music_sizing order by 1 asc"
    elif filter_name == 'gender':
        sql =  "select distinct gender from music_sizing"

    result = db.engine.execute(sql)
    datums  = []
    for row in result:
        datum =  {filter_name: row[0]}
        for item in filter_values['countries']:
            if item == row[0]:
                datum['selected'] = 'selected'
                break;
            else: 
                datum['selected'] = False
        datums.append(datum)
    return datums


# --------------------------------------------------------------------------------
# API: Endpoints which return data results or filtering selections


@app.route('/appledash/api/genderpct.json', methods=['GET','POST'])
def apple_gender_pct():

    filter_values = apple_initialize_filter_values()
    filter_sql    = apple_initialize_filter_sql()

    filter_values = apple_update_filter_values(filter_values)
    filter_sql    = apple_update_filter_sql(filter_values, filter_sql)

    measure = request.form.get('measure') #spotify or apple music

    sql =  "select \
              num.gender, \
              cast(round(sum(case when num.measure = '%s' then num.subscribers else 0 end) * 100 / \
                   max(case when den.measure = '%s' then den.subscribers else 0 end),0) as signed) measure_pct \
            from ( \
                select \
                  measure, \
                  sum(subscribers) subscribers \
                from music_sizing \
                where measure in ('spotify', 'apple music') \
                         %s \
                         %s \
                         %s \
                group by 1 \
            ) den inner join ( \
                select \
                  measure, \
                  gender, \
                  sum(subscribers) subscribers \
                from music_sizing \
                where measure in ('spotify', 'apple music') \
                         %s \
                         %s \
                         %s \
                group by 1,2 \
            ) num on num.measure = den.measure \
            group by 1 \
            order by 1 asc"  % (measure, measure, \
                                filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'], \
                                filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'])
    result = db.engine.execute(sql)

    data = []
    datasets = []
    countries  = []
    measure1_data  = []
    measure2_data = []
    for row in result:
        countries.append(row[0])
        measure1_data.append(row[1])

    backgroundColor = ['#ce3535','#2219ef']
    measure1 = dict (
        label = measure,
        data  = measure1_data,
        backgroundColor = backgroundColor
    )

    datasets.append(measure1)
    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)


@app.route('/appledash/api/agepct.json', methods=['GET','POST'])
def apple_age_pct():

    filter_values = apple_initialize_filter_values()
    filter_sql    = apple_initialize_filter_sql()

    filter_values = apple_update_filter_values(filter_values)
    filter_sql    = apple_update_filter_sql(filter_values, filter_sql)

    sql =  "select \
              num.age_range, \
              cast(round(sum(case when num.measure = 'spotify' then num.subscribers else 0 end) * 100 / \
                   max(case when den.measure = 'spotify' then den.subscribers else 0 end),0) as signed) sc_pct, \
              cast(round(sum(case when num.measure = 'apple music' then num.subscribers else 0 end) * 100 / \
                   max(case when den.measure = 'apple music' then den.subscribers else 0 end),0) as signed) ig_pct \
            from ( \
                select \
                  measure, \
                  sum(subscribers) subscribers \
                from music_sizing \
                where measure in ('spotify', 'apple music') \
                         %s \
                         %s \
                         %s \
                group by 1 \
            ) den inner join ( \
                select \
                  measure, \
                  CONCAT(age_min, '-', age_max) age_range, \
                  sum(subscribers) subscribers \
                from music_sizing \
                where measure in ('spotify', 'apple music') \
                         %s \
                         %s \
                         %s \
                group by 1,2 \
            ) num on num.measure = den.measure \
            group by 1 \
            order by 1 asc" % (filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'], \
                               filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'])

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
        label = 'spotify',
        data  = measure1_data,
        backgroundColor = "#04cf64"
    )
    measure2 = dict (
        label = 'apple music',
        data  = measure2_data,
        backgroundColor = "#740d69"
    )
    datasets.append(measure1)
    datasets.append(measure2)

    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)


@app.route('/appledash/api/countrypenetration.json', methods=['GET','POST'])
def apple_country_penetration():

    filter_values = apple_initialize_filter_values()
    filter_sql    = apple_initialize_filter_sql()

    filter_values = apple_update_filter_values(filter_values)
    filter_sql    = apple_update_filter_sql(filter_values, filter_sql)

    sql =  "select \
              country, \
              cast( sum(case when measure = 'spotify' then subscribers else 0 end) as signed) sc_subscribers, \
              cast( sum(case when measure = 'apple music' then subscribers else 0 end) as signed) ig_subscribers, \
              cast(round(sum(case when measure = 'spotify' then subscribers else 0 end) * 100 / \
                   sum(case when measure = 'ios' then subscribers else 0 end),0) as signed) sc_pen, \
              cast(round(sum(case when measure = 'apple music' then subscribers else 0 end) * 100 / \
                   sum(case when measure = 'ios' then subscribers else 0 end),0) as signed) ig_pen, \
              cast( sum(case when measure = 'ios' then subscribers else 0 end) as signed) ios \
            from music_sizing \
            where measure in ('spotify', 'apple music', 'ios') \
             %s\
             %s\
             %s\
            group by 1 \
            order by 2 desc \
            limit 10" % (filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'])

    result = db.engine.execute(sql)

    data = []
    datasets = []
    countries  = []
    measure1_data  = []
    measure2_data = []
    for row in result:
        countries.append(row[0])
        measure1_data.append(row[3])
        measure2_data.append(row[4])

    measure1 = dict (
        label = 'spotify',
        data  = measure1_data,
        backgroundColor = "#04cf64"
    )
    measure2 = dict (
        label = 'apple music',
        data  = measure2_data,
        backgroundColor = "#740d69"
    )
    datasets.append(measure1)
    datasets.append(measure2)

    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)


@app.route('/appledash/api/countrysubscribers.json', methods=['GET','POST'])
def apple_country_subscribers():

    filter_values = apple_initialize_filter_values()
    filter_sql    = apple_initialize_filter_sql()

    filter_values = apple_update_filter_values(filter_values)
    filter_sql    = apple_update_filter_sql(filter_values, filter_sql)

    sql =  "select \
              country, \
              cast( sum(case when measure = 'spotify' then subscribers else 0 end) as signed) sc_subscribers, \
              cast( sum(case when measure = 'apple music' then subscribers else 0 end) as signed) ig_subscribers \
            from music_sizing \
            where measure in ('spotify', 'apple music') \
             %s\
             %s\
             %s\
            group by 1 \
            order by 2 desc \
            limit 10" % (filter_sql['genders'], filter_sql['age_ranges'], filter_sql['countries'])

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
        label = 'spotify',
        data  = measure1_data,
        backgroundColor = "#04cf64"
    )
    measure2 = dict (
        label = 'apple music',
        data  = measure2_data,
        backgroundColor = "#740d69"
    )
    datasets.append(measure1)
    datasets.append(measure2)

    data = dict (
        labels    = countries,
        datasets  = datasets
    )

    return jsonify(data)

