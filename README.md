# Overview

This is the app that runs on excelninja.com. At the moment it only does a few things

1. Redirects users who visit excelninja.com to John Marsland's Linked In
2. Powers a few view layers which load exploratory dashboards
2. Has api endpoints which power these dashboards


# Getting Started

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python localapp.py
```

If you're running locally, you'll also need to create a file called settingslocal.py and add the following authentication credentials

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
print "Loading " + __file__

from excelninja import app

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}@{hostname}/{database}".format(
    username="USERNAME",
    password="PASSWORD",
    hostname="HOSTNAME",
    database="DATABASE?charset=utf8mb4",
)

app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

app.config['SECRET_KEY'] = ''
```





