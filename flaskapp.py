import os
import json
from bson import json_util
import datetime
from time import mktime
from flask import Flask, request, flash, url_for, redirect, Response, \
     render_template, abort, send_from_directory
from mongodao import Mongodao
import time

from flask_cache import Cache
app = Flask(__name__)
# Check Configuring Flask-Cache section for more details
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
dao = Mongodao()


json.JSONEncoder.default = lambda self,obj: (int(mktime(obj.timetuple())) if isinstance(obj, datetime.datetime) else None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()
