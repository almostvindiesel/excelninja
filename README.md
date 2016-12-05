# Overview

This is the app that runs on excelninja.com. At the moment it only does two things

1. Redirects users who visit the homepage to John Marsland's Linked In
2. Runs an example dashboard (at homepage.com/dash) that compares Estimated SnapChat DAU to Instagram DAU


# Installation

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





