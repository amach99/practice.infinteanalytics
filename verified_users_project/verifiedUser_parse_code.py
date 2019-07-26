import ndjson
import pprint

loc_ASIA [] = ''
loc_AMERICAS [] = ''
loc_EU [] = ''


with open('verifiedAccounts_subset') as input:
    data = ndjson.load(input)
    length = len(data)
    tweet_counter = 0
    while tweet_counter < length:
        name = data[tweet_counter]['user']['name']
        location = data[tweet_counter]['user']['location']
        language = data[tweet_counter]['user']['lang']
        print('Name: ', name,'/Loc: ', location,'/Lang: ', language)
        print('\n')
        tweet_counter += 1






