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
def gettwit(keyword):
    import twittertest as tw
    result = tw.scrapTweets(keyword=keyword, mongodao=dao)

    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

@app.route("/getlists/")
@cache.cached(300, key_prefix='getlists')
def getlists():
    '''
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
    '''
    pos_list, neg_list = dao.get_senti_for_all_tickers()
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
    from threading import Thread
    print('start threading...', file=sys.stdout)
    thread = Thread(target = gen_senti_thread)
    thread.start()
    print('end threading...', file=sys.stdout)
    
    return Response('Senti generation running in the background...', mimetype='application/json')

def gen_senti_thread():
    import sentiment_classifier as sc
    senti = sc.SentimentClassifier()
    senti.run_senti_for_all_ticker(dao)
    
@app.route("/get_sample_tweets/<keyword>")
def get_sample_tweets(keyword):
    
    senti_tweet = dao.get_senti_tweet_by_keyword(keyword)
    if senti_tweet:
        listOfTweets = senti_tweet.get('tweetsByDate')
        pos_list = set()
        neg_list = set()
        for tweet in listOfTweets:
            sentiVal = tweet.get('senti', None)
            if sentiVal:
                if sentiVal == 'pos':
                    pos_list.add(tweet.get('tweet'))
                else:
                    neg_list.add(tweet.get('tweet'))
    
        
        result = {'neg_list':list(neg_list)[0:5], 'pos_list':list(pos_list)[0:5]}
    else:
        result = {}
    
    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                , mimetype='application/json')

@app.route("/derek/")
def derek():
    
    import sentiment_classifier as sc
    sentClassifier = sc.SentimentClassifier()
    senti = sentClassifier.classify_tweet("Williams Cos. downgraded by  Investment Research to hold")
    if len(senti) > 0:
        senti = senti[0]
    print(senti)
    
    return Response(json.dumps(senti, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

@app.route("/scrap/")
def scrap():
    
    import ticker_scrapper as ts
    market, dict_tickers_by_sector = ts.get_snp500(dao)
    result = []
    for key, val in dict_tickers_by_sector.items():
        result.extend(val)
    
    result.reverse()
    from threading import Thread
    print('start threading...', file=sys.stdout)
    thread = Thread(target = backend_scrapping, kwargs = {'arg':result})
    thread.start()
    print('end threading...', file=sys.stdout)
    
    return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                    , mimetype='application/json')

    
def backend_scrapping(arg):
    print('start....', file=sys.stdout)
    from time import sleep
    import twittertest as tw
    count = 0
    tickers = 0
    for keyword in arg:
        print('start getting [%s]' % keyword, file=sys.stdout)
        try:
            pages = tw.scrapTweets(keyword=keyword, mongodao=dao)
        except:
            print('processed %s tickers, sleep for 15 minutes' % tickers)
            count = 0
            pages = 0
            sleep(61*15)
        print('finish getting [%s]' % keyword, file=sys.stdout)
        count += pages
        tickers += 1
        if count >= 170 and count % 170 == 0:
            print('processed %s tickers, sleep for 15 minutes' % tickers)
            count = 0
            pages = 0
            sleep(61*15)
    print('all done')

@app.route("/hist_quote/<symbol>")
def hist_quote(symbol):

    interval_seconds = 60 * 60 * 24
    num_years = 1
    
    result = []
    symbol = symbol.upper()
    url_string = "http://www.google.com/finance/getprices?q={0}".format(symbol)
    url_string += "&i={0}&p={1}Y&f=d,o,h,l,c,v".format(interval_seconds,num_years)
    csv = urllib.urlopen(url_string).readlines()
    for bar in xrange(7,len(csv)):
        if csv[bar].count(',')!=5: continue
        offset,close,high,low,open_,volume = csv[bar].split(',')
        if offset[0]=='a':
            day = float(offset[1:])
            offset = 0
        else:
            offset = float(offset)
            open_,high,low,close = [float(x) for x in [open_,high,low,close]]
            dt = datetime.datetime.fromtimestamp(day+(interval_seconds*offset))
            result.append([dt,open_,high,	return Response(json.dumps(result, ensure_ascii=False).encode('utf8')
                , mimetype='application/json')
	  
if __name__ == '__main__':
    app.run()
