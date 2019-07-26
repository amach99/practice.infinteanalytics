import pandas as pd
import urllib.request
import json
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import time
import requests



def get_node(keyword):
    if ' ' in keyword:
     keyword =  keyword.replace(' ', '_')
    lowercase_keyword = keyword.lower()

    CN_node_url = 'http://api.conceptnet.io/uri?language=en&text='+lowercase_keyword
    CN_node = urllib.request.urlopen(CN_node_url)
    node = json.load(CN_node)

    node_check_url = 'http://api.conceptnet.io/'+node['@id']
    node_check = urllib.request.urlopen(node_check_url)
    checked_node = json.load(node_check)

    if checked_node.get('error') is not None:
        return None
    else:
        node_key = checked_node['@id']
        return node_key

'''
def get_insights(node: object, keyword: object) -> object:
    insights = []
    conceptnet_url = 'http://api.conceptnet.io/related/'+node+'?filter=/c/en'
    json_obj = urllib.request.urlopen(conceptnet_url)
    data = json.load(json_obj)

    for item in data['related']:
        split_item = item['@id'].split('/')
        if '_' in split_item[-1]:
            split_item[-1] = split_item[-1].replace('_', ' ')

# jaccard distance
        lowercase_interest = keyword.lower()
        if ' ' in lowercase_interest:
            double_split_item = split_item[-1].split(' ')
            split_interest = lowercase_interest.split(' ')
            jaccard_set1 = set(double_split_item)
            jaccard_set2 = set(split_interest)
            jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)
        else:
            jaccard_set1 = set(split_item[-1])
            jaccard_set2 = set(lowercase_interest)
            jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)

# if insight is too similar, move on to the next insight
        if jd < 0.3 or lowercase_interest.find(split_item[-1]) > -1:
            continue


# word stemming
        ps = PorterStemmer()
        insight_word_stem = word_tokenize(split_item[-1])
        query_word_stem = word_tokenize(lowercase_interest)

        stop_loop = 0
        for word in query_word_stem:
            if stop_loop == 0:
                query_root = ps.stem(word)
                for word in insight_word_stem:
                    insight_root = ps.stem(word)
                    if query_root == insight_root:
                        stop_loop = 1
                        break
        if stop_loop == 1:
            continue

        insights.append(split_item[-1])

    return insights[:10]   # change this line to determine how many insights to return

'''

def get_related_urls(node):
    related_urls = []
    conceptnet_url = 'http://api.conceptnet.io'+node+'?format=json'
    obj = requests.get(conceptnet_url).json()
    dict_keys = obj.keys()
    pg_len = len(obj['edges'])
    edge_num = 1  # conceptnet node number ( 20 per pg )
    stop_loop = 0

    while stop_loop is 0:
        if 'view' in dict_keys:
            # move on to next page
            if 'nextPage' in obj['view']:
                nextPG = 'http://api.conceptnet.io' + obj['view']['nextPage']

                if edge_num == pg_len:
                    status = requests.get(nextPG).status_code
                    if status == 200:
                        print('Success!, next page opened\n', nextPG)
                        obj = requests.get(nextPG).json()
                        edge_num = 1
                        pg_len = len(obj['edges'])
                        continue
                    elif status == 404:
                        print('Not Found. Failed to open next page\n')
         # if link to next page is not found, sets the loop to run one more time for the last page
            else:
                stop_loop = 1
        else:
            stop_loop = 1

        while edge_num < pg_len:
            # iterate thru edge nodes on page
            print(edge_num)
            edge = obj['edges'][edge_num]
            # check to see if url is valid and opens correctly
            if 'site_available' in edge['end']:
                if edge['end']['site_available'] is True:
                    print(edge)
                    potential_url = obj['edges'][edge_num]['end']['@id']
                    print(potential_url)
                    url_status = requests.get(potential_url).status_code
                    print(url_status)
                    if url_status == 200:
                        print('Success!')
                        related_urls.append(potential_url)
                    elif url_status == 404:
                        print('Not Found.')

            edge_num += 1
            print('\n')

    return related_urls

###########################################

def get_insights(node: object, keyword: object) -> object:
    insights = []
    conceptnet_url = 'http://api.conceptnet.io/related/'+node+'?filter=/c/en'
    json_obj = urllib.request.urlopen(conceptnet_url)
    data = json.load(json_obj)
    dict_keys = data['@id'].keys()
    print(dict_keys)
    data_len = len(data['edges'])
    edge_counter = 1
    stop_check = 0

# todo fix bugs in page iterating loop

    while stop_check is 0:
        if 'view' in dict_keys:
            # move on to next page
            if 'nextPage' in data['view']:
                nextPG = 'http://api.conceptnet.io' + data['view']['nextPage']

                if edge_counter == data_len:
                    status = requests.get(nextPG).status_code
                    if status == 200:
                        print('Success!, next page opened\n', nextPG)
                        data = requests.get(nextPG).json()
                        edge_counter = 1
                        data_len = len(data['edges'])
                        continue
                    elif status == 404:
                        print('Not Found. Failed to open next page\n')
         # if link to next page is not found, sets the loop to run one more time for the last page
            else:
                stop_check = 1
        else:
            stop_check = 1


        while edge_counter < data_len:
            for item in data['related']:
                split_item = item['@id'].split('/')
                if '_' in split_item[-1]:
                    split_item[-1] = split_item[-1].replace('_', ' ')

        # jaccard distance
                lowercase_interest = keyword.lower()
                if ' ' in lowercase_interest:
                    double_split_item = split_item[-1].split(' ')
                    split_interest = lowercase_interest.split(' ')
                    jaccard_set1 = set(double_split_item)
                    jaccard_set2 = set(split_interest)
                    jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)
                else:
                    jaccard_set1 = set(split_item[-1])
                    jaccard_set2 = set(lowercase_interest)
                    jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)

        # if insight is too similar, move on to the next insight
                if jd < 0.3 or lowercase_interest.find(split_item[-1]) > -1:
                    edge_counter += 1
                    continue


        # word stemming
                ps = PorterStemmer()
                insight_word_stem = word_tokenize(split_item[-1])
                query_word_stem = word_tokenize(lowercase_interest)

                stop_loop = 0
                for word in query_word_stem:
                    if stop_loop == 0:
                        query_root = ps.stem(word)
                        for word in insight_word_stem:
                            insight_root = ps.stem(word)
                            if query_root == insight_root:
                                stop_loop = 1
                                break
                if stop_loop == 1:
                    edge_counter += 1
                    continue


                insights.append(split_item[-1])
                edge_counter += 1


        return insights[:10]   # change this line to determine how many insights to return



###########################################
# dict_keys(['@context', '@id', 'edges', 'error'])


keyword = 'spider man'
node = get_node(keyword)
print(node, '\n')
insights = get_insights(node, keyword)
related_urls = get_related_urls(node)

print(insights)
print(related_urls)


'''

df = pd.read_csv('list_of_related_terms_conceptnet_input - Sheet1.tsv', sep='\t')

for index, row in list(df.iterrows()):
    time.sleep(2)
    keyword = row['KEYWORD']
    print('KEYWORD: '+keyword)
    node = get_node(keyword)
    if node is None:
        print("Node does not exist\n")
        df.iloc[index, [1]] = 'Node does not exist'
        df.to_csv('list_of_related_terms_conceptnet_output.tsv', sep='\t')
        continue
    data = get_insights(node, keyword)
    related_urls_for_data = get_related_urls(node)

    row['CONCEPT_NET NODE'] = node
    row['INSIGHTS'] = data
    row['RELATED URLS'] = related_urls_for_data
    print(row, '\n')
    df.iloc[index] = row

df.to_csv('list_of_related_terms_conceptnet_output.tsv', sep='\t')
print(df[:15])
'''