#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json  # or `import simplejson as json` if on Python < 2.6
import pymongo
import datetime
import os

p = '%Y-%m-%dT%H:%M:%S.%fZ'
    
class Mongodao:
    
    def __init__(self):
        from pymongo import MongoClient
        if os.environ.get('OPENSHIFT_GEAR_NAME', None):
            client = MongoClient('mongodb://admin:URUI3swsR-Lm@57864af57628e13523000169-jphackathon.rhcloud.com:52211/')
        else:
            client = MongoClient('mongodb://localhost:27017/')
        self.twits_db = client.twitsdb
        self.ticker_db = client.tickerdb
    
    def get_twit_by_keyword(self, keyword):
        if keyword:
            keyword = keyword.upper()
        twit = self.twits_db.twits.find_one({"keyword":keyword})
        if not twit:
            return {}
        else:
            del twit['_id']
            return twit
    
    def save_twit_by_keyword(self, keyword, twit):
        if keyword:
            keyword = keyword.upper()
        twitFromDb = self.twits_db.twits.find_one({"keyword":keyword})
        if twitFromDb:
            twit['_id'] = twitFromDb['_id']
        twit['lastUpdate'] = datetime.datetime.utcnow()
        self.twits_db.twits.save(twit)
        del twit['_id']
        del twit['lastUpdate']
        
    def save_senti_ticker_by_keyword(self, keyword, ticker):
        if keyword:
            keyword = keyword.upper()
        twitFromDb = self.twits_db.senti_tweets.find_one({"keyword":keyword})
        if twitFromDb:
            ticker['_id'] = twitFromDb['_id']
        ticker['lastUpdate'] = datetime.datetime.utcnow()
        self.twits_db.senti_tweets.save(ticker)

    def get_senti_ticker_by_keyword(self, keyword):
        if keyword:
            keyword = keyword.upper()
        print('getting ticker for %s' % keyword)
        if not keyword:
            return {}
        ticker = self.twits_db.senti_tweets.find_one({"keyword":keyword})
        
        if not ticker:
            return {}
        
        neg_count = 0
        pos_count = 0
        total_count = 0
        
        date_dict = dict()
        
        for x in ticker.get('tweetsByDate', None):
            if x:
                date = x.get('created_at', None)
                if date:
                    key = date[0:3]
                    value = date_dict.get(key, None)
                    if not value:
                        value = {'pos':0, 'neg':0, 'total':0}
                        date_dict[key] = value
                    value['total'] = value.get('total', 0) + 1
                    if x.get('senti') == 'neg':
                        value['neg'] = value.get('neg', 0) + 1
                    else:
                        value['pos'] = value.get('pos', 0) + 1
            
        #for key, value in sorted(mydict.items(), key=lambda (k,v): (v,k)):
        #    print "%s: %s" % (key, value)    
        result = []            
        for key, value in date_dict.items():
            tpc = value.get('pos', 0)
            tnc = value.get('neg', 0)
            ttc = value.get('total', tpc+tnc)
            tps = float(tpc/ttc)
            tns = float(tnc/ttc)
            result.append({'date':key, 'tpc':tpc, 'tnc':tnc, 'tps':tps, 'tns':tns})
        print(result)    
        return result   
        #{'date':'Wed Jul 06 12:32:31 +0000 2016', 'tpc':90, 'tnc':10, 'tps':0.9, 'tns':0.1}
        
        
    def get_senti_for_all_tickers(self):
        cursor = self.twits_db.senti_tweets.find()
        print("found %s senti tickers" % cursor.count())
        
        listTickerToSenti = []
        for ticker in cursor:
            neg_count = 0
            pos_count = 0
            total_count = 0            
            for x in ticker.get('tweetsByDate', None):

                if x:
                    if x.get('senti') == 'neg':
                        neg_count += 1
                    else:
                        pos_count += 1
                    total_count += 1
            listTickerToSenti.append({'ticker':ticker.get('keyword'), 'pos':float(pos_count/total_count), 'neg':neg_count/total_count})
        
        negSortList = sorted(listTickerToSenti, key=lambda item: (item.get('pos')))
        n = lambda item: {'ticker':item.get('ticker'), 'senti':round(item.get('neg', 0) * -1, 2)}
        neg_list = [n(item) for item in negSortList[0:5]]
        posSortList = sorted(listTickerToSenti, key=lambda item: (item.get('pos')), reverse=True)
        p = lambda item: {'ticker':item.get('ticker'), 'senti':round(item.get('pos'), 2)}
        pos_list = [p(item) for item in posSortList[0:5]]
        print ("%s" % pos_list) 
        print ("%s" % neg_list) 
        return pos_list, neg_list
        #print(listTickerToSenti)
        #pos_list.append({'ticker':'APPL', 'senti':0.9})
        
    def save_ticker_by_key(self, key, val):
        if key:
            key = key.upper()
        tickersFromDb = self.ticker_db.tickers.find_one({"key":key})
        if not tickersFromDb:
            tickersFromDb = dict()
            tickersFromDb['key'] = key
        tickersFromDb['tickers'] = val
        self.ticker_db.tickers.save(tickersFromDb)
    
    def get_ticker_by_key(self, key):
        if key:
            key = key.upper()
        tickersFromDb = self.ticker_db.tickers.find_one({"key":key})
        if tickersFromDb:
            return tickersFromDb.get('tickers', None)

    def get_all_tweets(self):
        list = []
        cursor = self.twits_db.twits.find()

        print("found %s tickers" % cursor.count())
        f = lambda ws: ws.get('tweet', None)
        for tweet in cursor:
            list.extend(f(x) for x in tweet.get('tweetsByDate', None))
        print("found %s tweets" % len(list))
        return list
    
    def get_all_tweetsByDate(self):
        cursor = self.twits_db.twits.find()
        print("found %s tickers" % cursor.count())
        return cursor
     
if __name__ == "__main__":

    mongodao = Mongodao()
    mongodao.get_senti_for_all_tickers()
    #mongodao.get_senti_ticker_by_keyword('MON')
    #print(mongodao.get_all_tweets())
