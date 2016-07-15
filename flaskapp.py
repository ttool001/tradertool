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
    return render_template('userInterface.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('UI/', resource)

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

@app.route("/getlists/")
def getlists():
    
    pos_list = []
    pos_list.append({'ticker':'APPL', 'senti':0.9})
    pos_list.append({'ticker':'JPM', 'senti':0.89})
    pos_list.append({'ticker':'IBM', 'senti':0.79})
    pos_list.append({'ticker':'V', 'senti':0.79})
    pos_list.append({'ticker':'C', 'senti':0.69})
    pos_list.append({'ticker':'GOOG', 'senti':0.69})
    pos_list.append({'ticker':'JOBS', 'senti':0.59})
    pos_list.append({'ticker':'FB', 'senti':0.59})
    pos_list.append({'ticker':'MSFT', 'senti':0.49})
    
    neg_list = []
    neg_list.append({'ticker':'SIRI', 'senti':-0.9})
    neg_list.append({'ticker':'FTR', 'senti':-0.77})
    neg_list.append({'ticker':'MNKD', 'senti':-0.76})
    neg_list.append({'ticker':'AMD', 'senti':-0.69})
    neg_list.append({'ticker':'INTC', 'senti':-0.59})
    neg_list.append({'ticker':'OPK', 'senti':-0.59})
    neg_list.append({'ticker':'MU', 'senti':-0.49})
    neg_list.append({'ticker':'HBAN', 'senti':-0.39})
    neg_list.append({'ticker':'NVAX', 'senti':-0.39})
    
    result = {'pos_list':pos_list, 'neg_list':neg_list}
    
    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')
    
if __name__ == '__main__':
    app.run()
