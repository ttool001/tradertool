
from __future__ import unicode_literals
import requests
import json
import csv
#import pyexcel
from requests_oauthlib import OAuth1
from mongodb.mongodao import Mongodao
import datetime
from urllib import request, parse, error

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "0XcvuiH335B3GpaJX8y96JCyB"
CONSUMER_SECRET = "LoxYBF96ISbS4TjofORK7lLFMbhegWbPAEmplHix2UZJl8m9aE"

OAUTH_TOKEN = "722527962743062529-LP1X9LMlTZD7FgoCPO04Lv0GfHET1sh"
OAUTH_TOKEN_SECRET = "AHGRxJTazZ7bnWndzWSxqbqHkYxwPArQR3CWKtONAz92q"

BASE_QUERY = 'https://api.twitter.com/1.1/search/tweets.json?'

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

# with open('berniesanderstest.csv', 'w',encoding="utf8") as f:
#     a = csv.writer(f)

def getTweets(keyword, mongodao, lang='en', count=1000, result_type='mixed'):
    #make sure keyword is valid
    
    if not keyword:
        return 'keyword needs to be valid'
    else:
        search_keyword = '$%s' % keyword
    twit = mongodao.get_twit_by_keyword(keyword)
    if twit:
        last_ts = twit['lastUpdate']
        if last_ts:
            now = datetime.datetime.now()
            if (now - last_ts) < datetime.timedelta(minutes = 15):
                del twit['lastUpdate']
                return twit
            
    oauth = get_oauth()
    
    encoded_params = parse.urlencode({'q':search_keyword, 'count':count, 'lang':lang, 'result_type':result_type})
    print('rest call to [%s]' % encoded_params)
    bernie_sander_tweets = requests.get(url=BASE_QUERY, params=encoded_params,  auth=oauth)
    new_json = bernie_sander_tweets.json()["statuses"]
    twitTexts = set()
    for i in new_json:
        for key,value in i.items():
            if(key=='text'):
                try:
                    encodedVal = str(value.encode('utf-8'))
                    twitTexts.add(encodedVal)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass                         
                    
    twit = {'keyword':keyword, 'twit':list(twitTexts)}
    mongodao.save_twit_by_keyword(keyword, twit)
    return twit        



if __name__ == "__main__":

    mongodao = Mongodao()
    print(getTweets('APPL', mongodao))

    '''
    for x in getTweets('APPL', mongodao):
        try:
            print(x)
        except UnicodeEncodeError as e:
            print('error happened %s', e)
            
    oauth = get_oauth()
    hillary_tweets = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q=HillaryClinton&count=200", auth=oauth)
    bernie_sander_tweets = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q=BernieSanders&count=200", auth=oauth)
    trump_tweets  = requests.get(url="https://api.twitter.com/1.1/search/tweets.json?q=DonaldTrump&count=200", auth=oauth)
    new_json = bernie_sander_tweets.json()["statuses"]
    #fileBernie = open('bernieSanders.txt', 'wb')
    for i in new_json:
        for key,value in i.items():
            #pyexcel.save_as(array=key, dest_file_name='berniesanderstest.csv')
             if(key=='text'):
                 print (value)
                 #fileBernie.writelines(value.encode('utf-8'))
        #
        #             a.writerows(value)
        #print(i)
    '''