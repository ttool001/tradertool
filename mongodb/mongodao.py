#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json  # or `import simplejson as json` if on Python < 2.6
import pymongo
import datetime


p = '%Y-%m-%dT%H:%M:%S.%fZ'
    
class Mongodao:
    
    def __init__(self):
        from pymongo import Connection
        connection = Connection()
        #create db if it doesn't exists
        db = connection['twitsdb']
        collection = db['twits']
        
        from pymongo import MongoClient
        client = MongoClient('mongodb://admin:URUI3swsR-Lm@57864af57628e13523000169-jphackathon.rhcloud.com:52211/')
        #client = MongoClient('mongodb://localhost:27017/')
        self.twits_db = client.twitsdb
    
    def get_twit_by_keyword(self, keyword):
        twit = self.twits_db.twits.find_one({"keyword":keyword})
        if not twit:
            return {}
        else:
            del twit['_id']
            del twit['lastUpdate']
            return twit
    
    def save_twit_by_keyword(self, keyword, twit):
        twitFromDb = self.twits_db.twits.find_one({"keyword":keyword})
        if twitFromDb:
            twit['_id'] = twitFromDb['_id']
        epoch = datetime.datetime.utcnow()
        twit['lastUpdate'] = epoch
        self.twits_db.twits.save(twit)
        del twit['_id']
        del twit['lastUpdate']

        

if __name__ == "__main__":

    mongodao = Mongodao()
    mocktwit = []
    mocktwit.append('#APPL is going to drop like fly because iphone 7 is not impressive')
    twit = {'keyword':'APPL', 'twits':mocktwit}
    mongodao.save_twit_by_keyword('APPL', twit)
    result = mongodao.get_twit_by_keyword('APPL')
    print(result)
