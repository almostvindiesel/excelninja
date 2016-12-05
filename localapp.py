print "Loading localapp.py"

import os
os.environ['EXCELNINJA_ENVIRONMENT'] = 'local'

from excelninja import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
