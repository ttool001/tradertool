#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json  # or `import simplejson as json` if on Python < 2.6
import pymongo
import datetime


p = '%Y-%m-%dT%H:%M:%S.%fZ'
    
class Mongodao:
    
    def __init__(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://admin:URUI3swsR-Lm@57864af57628e13523000169-jphackathon.rhcloud.com:52211/')
        #client = MongoClient('mongodb://localhost:27017/')
        self.twits_db = client.twitsdb
        self.ticker_db = client.tickerdb
    
    def get_twit_by_keyword(self, keyword):
        twit = self.twits_db.twits.find_one({"keyword":keyword})
        if not twit:
            return {}
        else:
            del twit['_id']
            return twit
    
    def save_twit_by_keyword(self, keyword, twit):
        twitFromDb = self.twits_db.twits.find_one({"keyword":keyword})
        if twitFromDb:
            twit['_id'] = twitFromDb['_id']
        twit['lastUpdate'] = datetime.datetime.utcnow()
        self.twits_db.twits.save(twit)
        del twit['_id']
        del twit['lastUpdate']

    def save_ticker_by_key(self, key, val):
        tickersFromDb = self.ticker_db.tickers.find_one({"key":key})
        if not tickersFromDb:
            tickersFromDb = dict()
            tickersFromDb['key'] = key
        tickersFromDb['tickers'] = val
        self.ticker_db.tickers.save(tickersFromDb)
    
    def get_ticker_by_key(self, key):
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
    
if __name__ == "__main__":

    mongodao = Mongodao()
    print(mongodao.get_all_tweets())
