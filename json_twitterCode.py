import json
import requests


class myTweet:
    def __init__(self, nodeID, tweetID, username, date, type, emotion, resource, text):
        self.nodeID = nodeID
        self.tweetID = tweetID
        self.twitter_username = username
        self.date = date
        self.type = type
        self.emotion = emotion
        self.resource = resource
        self.text = text


def get_related_terms(resource, seeAlso_url):

    if 'resource' in resource:
        new_resource = resource.replace('resource', 'data')
    # print(new_resource)

    json_resource = new_resource + '.json'
    print(json_resource)
    print('\n')

    with requests.get(json_resource) as response:
        data = response.json()
        # print(type(response))
        response.encoding = 'utf-8'
        data_text = response.text
        data_text = data_text.replace(',', '\n')
        # print(data_text, '\n')

        data_keys = data.keys()
        data_key_list = list(data_keys)
        # print(data_key_list, len(data_key_list))

        data_values = data.values()
        print('\n')
        # print(list(data_values))

        x = 0
        related_terms = []
        for line in response.iter_lines():
            encoded_seeAlso_url = seeAlso_url.encode()
            if encoded_seeAlso_url in line:  # finding the links for the 'seeAlso' api's
                print('line #:', x)
                important_line = line.split()
                related_url = important_line[0]
                keyword = str(related_url).split('/')
                related_terms.append(keyword[-1])
                # print(keyword[-1])
                print('\n')
                print(related_url, '\n')  # finally got the url for related terms!!
            x += 1

        # getting more related terms that are stored elsewhere on the website
        # checking to make sure data[resource][seeAlso_url] is a (valid key,value) pair
        if seeAlso_url in data[resource]:
            data_resource_len = len(data[resource][seeAlso_url])
            y = 0
            while y < data_resource_len:
                if seeAlso_url in data[resource]:
                    related_term = data[resource][seeAlso_url][y]['value'].split('/')[-1]
                    related_terms.append(related_term)
                else:
                    print('NADA\n')
                y += 1

        newRelatedTermsList = [item.replace('\'', '') for item in related_terms]
        return newRelatedTermsList


with open('twitter_in_json.json', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)
    length = len(data['RDF']['Description'])
    index = 0
    while index < length:
        keys = data['RDF']['Description'][index]
        print('Index #:', index, ' ', keys, '\n')

        if '_rdf:nodeID' in keys:  # nodeID of tweet in tweetskb database
            myTweet.nodeID = keys['_rdf:nodeID']
            print('NodeID:', myTweet.nodeID)
        if 'hasMatchedURI' in keys:  # dbpedia resource page url
            myTweet.resource = keys['hasMatchedURI']['_rdf:resource']
            seeAlso_url = data['RDF']["_xmlns:rdfs"] + 'seeAlso'
            print('RESOURCE:', myTweet.resource)
            # if resource url is found, get related terms
            related_terms = get_related_terms(myTweet.resource, seeAlso_url)
            print('list of related terms:')
            print(related_terms, '\n')
        else:
            print('RESOURCE: N/A')
        if 'detectedAs' or 'label' in keys:  # any text retrieved from the tweet
            if 'detectedAs' in keys:
                myTweet.text = keys['detectedAs']['__text']
                print('TEXT:', myTweet.text)
            elif 'label' in keys:
                myTweet.text = keys['label']['__text']
                print('TEXT:', myTweet.text)
        else:
            print('TEXT: N/A')
        if 'type' in keys:  # type of the identified subject of the tweet
            resource_url = keys['type']['_rdf:resource']
            resource_type = resource_url.split('/')
            split_type = resource_type[-1]
            myTweet.type = split_type
            print('TYPE:', myTweet.type)
        else:
            print('TYPE: Unknown')
        if 'id' in keys:  # tweet id
            myTweet.tweetID = keys['id']['__text']
            print('TweetID:', myTweet.tweetID)
        else:
            print('TweetID: Unknown')
        if 'has_creator' in keys:  # username of person who posted the tweet
            myTweet.twitter_username = keys['has_creator']['_rdf:nodeID']
            print('USERNAME:', myTweet.twitter_username)
        else:
            print('USERNAME: Unknown')
        if 'created' in keys:  # date tweet was posted
            myTweet.date = keys['created']['__text']
            print('DATE:', myTweet.date)
        else:
            print('DATE: Unknown')
        if 'confidence' in keys:   # positive sentiment range: [+1, +5] || negative sentiment range: [-1,-5]
            sentiment_range = keys['confidence']['__text']
            if '-' not in sentiment_range:
                myTweet.emotion = 'EMOTION: positive emotion'
            elif '-' in sentiment_range:
                myTweet.emotion = 'EMOTION: negative emotion'
            print(myTweet.emotion)
        else:
            print('EMOTION: N/A')

        print('\n')
        index += 1  # move on to the next child in the twitter_in_json.json file to explore its contents

    #resource = "http://dbpedia.org/resource/Abortion"
    #resource = 'http://dbpedia.org/resource/French_people'




'''    
if 'resource' in resource:
        new_resource = resource.replace('resource', 'data')
    # print(new_resource)

    json_resource = new_resource + '.json'
    print(json_resource)
    print('\n')

    with requests.get(json_resource) as response:
        response.encoding = 'utf-8'
        data = response.json()
        # print(type(response))
        data_text = response.text
        data_text = data_text.replace(',', '\n')
        #print(data_text, '\n')

        data_keys = data.keys()
        #print(data_keys)
        data_key_list = list(data_keys)
        print(data_key_list, len(data_key_list))

        data_values = data.values()
        print('\n')
        #print(data_values)


        if seeAlso_url in data_text:
            print('YES!\n')
        else:
            print('NADA\n')

        x = 0
        related_terms = []
        for line in response.iter_lines():
            encoded_seeAlso_url = seeAlso_url.encode()
            if encoded_seeAlso_url in line:  # finding the links for the seeAlso api's
                print('line #:', x)
                important_line = line.split()
                print(important_line)
                related_url = important_line[0]
                related_url = related_url.decode('utf-8')
                keyword = str(related_url).split('/')
                related_terms.append(keyword[-1])
                print(keyword[-1])
                print('\n')
                print(related_url, '\n')  # finally got the url for related terms!!
            x += 1
        #print(related_terms, '\n')



        newRelatedTermsList = [item.replace('\'', '') for item in related_terms]
        return newRelatedTermsList
'''