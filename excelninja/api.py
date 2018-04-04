#!/usr/bin/env python
# -*- coding: utf-8 -*-
print "Loading " + __file__

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

# Google API
# from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None
# ---------------




@app.route('/api/v1/recipes', methods=['GET'])
def get_recipes():


	# If modifying these scopes, delete your previously saved credentials
	# at ~/.credentials/drive-python-quickstart.json
	SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Drive API Python Quickstart'


	def get_credentials():
		print "get_credentials..."

		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									   'drive-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials

	def extract_recipes():
		print "main_api..."

		"""Shows basic usage of the Google Drive API.

		Creates a Google Drive API service object and outputs the names and IDs
		for up to 10 files.
		"""
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('drive', 'v2', http=http)

		parents_query = "'1fMHrwD1J3-WhV7d-HIqbvmPhxomlP6k-' in parents or '1Gv0h9svXbcAw86fOJlqkHHfgN5_U8r-C' in parents or '1iprey3gooBGeOP3Sc2UcoHsLwOGSBeK4' in parents"

		results = service.files().list(maxResults=30,q=parents_query).execute()
		#results = service.files().list(maxResults=30).execute()
		items = results.get('items', [])
		files = []
		if not items:
			print('No files found.')
		else:

			print('Files:')
			for item in items:
				if item['mimeType'] == 'application/vnd.google-apps.document' and item['explicitlyTrashed'] == False:
					print item['title']
					files.append({
						'id':item['id'], 
						'mimeType': item['mimeType'], 
						'name':item['title'],
						'parent':item['parents'][0]['id'],
						'starred': item['labels']['starred'],
						'version' : int(item['version'])
					})
				# files.append(item)
				
				#print item['parents']['id']
		return files

	files = []
	try:
		files = extract_recipes()
		files = sorted(files, key=lambda k: k['version'], reverse=True) 
		msg = 'success'
	except Exception:
		print "Something went wrong", Exception 
		msg = 'failure'

	return jsonify({'data':files,'msg':msg})







