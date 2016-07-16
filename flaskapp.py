import json
from flask import Flask, request, flash, url_for, redirect, Response, \
     render_template, abort, send_from_directory
from mongodb import mongodao
from flask_cache import Cache
import sys
from flask_cors import CORS, cross_origin

'''
import logging
from logging.handlers import RequiredHandler

file_handler = RequiredHandler(...)
file_handler.setLevel(logging.WARNING)

app.logger.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
'''

dao = mongodao.Mongodao()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
    
@app.route("/getticker/<keyword>")
def getticker(keyword):
    
    pos_list = dao.get_senti_ticker_by_keyword(keyword)
    '''
    pos_list.append({'date':'Wed Jul 06 12:32:31 +0000 2016', 'tpc':90, 'tnc':10, 'tps':0.9, 'tns':0.1})
    pos_list.append({'date':'Tue Jul 05 12:32:31 +0000 2016', 'tpc':80, 'tnc':20, 'tps':0.8, 'tns':0.2})
    pos_list.append({'date':'Mon Jul 04 12:32:31 +0000 2016', 'tpc':70, 'tnc':30, 'tps':0.7, 'tns':0.3})
    '''
    return Response(json.dumps(pos_list, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')
    
@app.route("/gen_senti/")
def gen_senti():
    from senti import StockSenti
    senti = StockSenti()
    senti.run_senti_for_all_ticker(dao)
    return Response('Senti generated', mimetype='application/plain')

@app.route("/scrap/")
def scrap():
    
    import ticker_scrapper as ts
    market, dict_tickers_by_sector = ts.get_snp500(dao)
    result = []
    for key, val in dict_tickers_by_sector.items():
        result.extend(val)
    
    from threading import Thread
    print('start threading...', file=sys.stdout)
    thread = Thread(target = backend_scrapping, kwargs = {'arg':result})
    thread.start()
    print('end threading...', file=sys.stdout)
    
    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

@app.route("/scrapremote/")
def scrapremote():
    
    import ticker_scrapper as ts
    market, dict_tickers_by_sector = ts.get_snp500(dao)
    result = []
    for key, val in dict_tickers_by_sector.items():
        result.extend(val)
    
    from threading import Thread
    print('start threading...', file=sys.stdout)
    thread = Thread(target = remote_scrapping, kwargs = {'list':result})
    thread.start()
    print('end threading...', file=sys.stdout)
    
    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

def remote_scrapping(list):
    print('start remote scrapping')
    from time import sleep
    import requests
    count = 0
    for keyword in list:
        requests.get(url='python-jphackathon.rhcloud.com/gettwit/' % keyword)
        count += 1
        if count % 170 == 0:
            print('sleep for 15 minutes')
            sleep(930)
    
def backend_scrapping(arg):
    print('start....', file=sys.stdout)
    from time import sleep
    import twittertest as tw
    count = 0
    for keyword in arg:
        print('start getting [%s]' % keyword, file=sys.stdout)
        tw.getTweets(keyword=keyword, mongodao=dao)
        print('finish getting [%s]' % keyword, file=sys.stdout)
        count += 1
        if count % 175 == 0:
            print('sleep for 16 minutes')
            sleep(60*16)
    print('all done')
    
if __name__ == '__main__':
    app.run()
