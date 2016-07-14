import json
from flask import Flask, request, flash, url_for, redirect, Response, \
     render_template, abort, send_from_directory
from mongodb import mongodao
from flask_cache import Cache
dao = mongodao.Mongodao()
app = Flask(__name__)

# Check Configuring Flask-Cache section for more details
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app.config.from_pyfile('flaskapp.cfg')

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

@app.route("/gettwit/<keyword>")
#@cache.cached(300, key_prefix='gettwit')
def gettwit(keyword):
    import twittertest as tw
    result = tw.getTweets(keyword=keyword, mongodao=dao)

    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

if __name__ == '__main__':
    app.run()
