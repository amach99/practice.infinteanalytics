import pandas as pd
import urllib.request
import json
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import time
import requests

# keyword clusters
food = ['Whey',
        'Cookie',
        'Frito-Lay',
        'Potato chip',
        'Barley',
        'Low-carbohydrate diet',
        "Lay's",
        'Fried chicken',
        'aquafina',
        'pepsi',
        'kurkure',
        'mountain dew',
        'pepsico',
        'fanta',
        'soft drinks',
        'biscuits',
        "Mcdonald's",
        'pineapple',
        'sandwich',
        'bottled water',
        'kale',
        'coffeemaker',
        'tap water',
        'cortado',
        'ristretto',
        'watermelon',
        'ketchup',
        'cream soda',
        'pomegranate',
        'kiwi fruit',
        'chocolate chip',
        'lemon',
        'coca cola zero',
        'minute maid',
        'Nestle',
        'Sprite',
        'soft drinks',
        'doritos',
        'gatorade',
        'tropicana',
        'coca-cola',
        'schweppes',
        'diet coke',
        'powerade',
        'thumbs up'
        ]
sports = ['Sachin Tendulkar',
          'Virat Kohli',
          'Cristiano Ronaldo',
          'Ronaldinho',
          'FIFA World Cup',
          'Brazil national football team',
          'Indian national cricket team',
          'Argentina national football team',
          'Mahendra Singh Dhoni',
          'Juventus F.C.',
          'Cricket World Cup',
          'China national football team',
          'football',
          'copa del rey'
          ]
entertainers = ['Katie Holmes',
                'Leonardo DiCaprio',
                'Nelly',
                'Lana Del Rey',
                'Logan Paul',
                'AC/DC',
                'Jennifer Lawrence',
                'KSIOlajidebt',
                'Jason Momoa',
                'Morena Baccarin'
                ]
movies = ['Inception',
          'Doctor Strange',
          'The Matrix',
          'Hulk (comics)',
          'Avengers (comics)',
          'DEADPOOL: The Movie',
          'Marvel Studios',
          'Star Trek',
          'The Hunger Games',
          'Spider-Man 3',
          'Spider-Man',
          'WALL-E',
          'Spider-Man 2',
          'Spider-Man (2002 film)',
          'Star Trek: The Original Series',
          'The Hunger Games (film)',
          'Iron Man 2',
          'Logan',
          'Iron Man',
          'The Amazing Spider-Man (2012 film)',
          'Deadpool',
          'The Avengers (2012 film)',
          'Marvel Entertainment',
          'Ghost Rider',
          'Fantastic Four',
          'Black Panther (comics)',
          'Thor (film)',
          'The Wolverine (film)',
          'Iron Man 3',
          'Captain America: The Winter Soldier',
          'Guardians of the Galaxy (film)',
          'Avengers: Age of Ultron',
          'Ant-Man (film)',
          'Fantastic Beasts and Where to Find Them (film)',
          'The Amazing Spider-Man 2',
          'The karate kid',
          'Ghostbusters'
          ]
fictional_char = ['Wolverine (character)',
                  'Luke Skywalker',
                  'Doctor Strange',
                  'Iron Man',
                  'Hulk',
                  'Spiderman'
                  ]
videoGames = ['Overwatch (video game)',
              'Uncharted',
              'Devil May Cry',
              'Grand Theft Auto: San Andreas',
              'Call of Duty: Black Ops',
              'God of War (series)',
              'Call of Duty: World at War',
              'Minecraft',
              "Assassin's Creed (video game)",
              'God of War (video game)',
              'Grand Theft Auto V',
              'Fortnite'
              ]
perfect_tags_list = ['The matrix','Avengers comics', 'Star trek', 'The hunger games', 'Logan', 'Iron man',
                     'Deadpool', 'Marvel entertainment', 'Ghost rider', 'Fantastic four', 'Thor film',
                     'Iron man 3', 'The karate kid', 'Ghostbusters','Overwatch video game','God of war series',
                     'Devil may cry', 'Minecraft', 'Wolverine character', 'Luke skywalker', 'Iron man', 'Hulk',
                     'Spiderman', 'Sachin tendulkar', 'Virat kohli', 'Cristiano ronaldo', 'Fifa world cup',
                     'Cricket world cup','Katie holmes', 'Logan paul', 'Jennifer lawrence', 'Jason momoa',
                     'Morena baccarin', 'Potato chip', 'Fried chicken', 'Pepsi', 'Mountain dew', 'Biscuits',
                     'Pineapple', 'Bottled water', 'Kale', 'Coffeemaker', 'Watermelon', 'Ketchup', 'Cream soda',
                     'Pomegranate', 'Lemon', 'Coca cola zero', 'Doritos', 'Diet coke']
nonFiction = [sports, entertainers, food]
fiction = [movies, videoGames, fictional_char]

# given a keyword, this function finds potential nodes
# INPUT: keyword = word that we want to find related terms for
def get_node(keyword):
    if '(' in keyword:
        keyword = keyword.replace('(', '')
        keyword = keyword.replace(')', '')
    if ' ' in keyword:
        keyword = keyword.replace(' ', '_')
    lowercase_keyword = keyword.lower()
    print('KEYWORD:', keyword)
    CN_node_url = 'http://api.conceptnet.io/uri?language=en&text='+lowercase_keyword
    CN_node = urllib.request.urlopen(CN_node_url)
    node = json.load(CN_node)

    node_check_url = 'http://api.conceptnet.io/'+node['@id']  # check to see if node is legitimate
    node_check = urllib.request.urlopen(node_check_url)
    checked_node = json.load(node_check)

    if checked_node.get('error') is not None:
        return None
    else:  # if node is verified return it
        node_key = checked_node['@id']
        return node_key


# iterates thru the nodes and if a url link is found, it stores it for the pandas df
# INPUT: node = matched node to keyword that is returned from get_node() function
def get_related_urls(node):
    related_urls = []
    conceptnet_url = 'http://api.conceptnet.io/'+node+'?format=json'
    obj = requests.get(conceptnet_url).json()
    dict_keys = obj.keys()
    pg_len = len(obj['edges'])
    edge_num = 1  # conceptnet node number (20 per pg)
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

        while edge_num < pg_len:  # iterate thru edge nodes on page
            #print(edge_num)
            edge = obj['edges'][edge_num]
            #print(edge)
            if 'site_available' in edge['end']:   # check to see if url is valid and opens correctly
                if edge['end']['site_available'] is True:
                    #print(edge)
                    potential_url = obj['edges'][edge_num]['end']['@id']
                    #print(potential_url)
                    url_status = requests.get(potential_url).status_code
                    #print(url_status)
                    if url_status == 200:
                        print('Success!')
                        related_urls.append(potential_url)
                    elif url_status == 404:
                        print('Not Found.')

            edge_num += 1
            print('\n')

    return related_urls


# gets insights for a keyword given a matched node
# INPUT: node = matched node from get_node() function
#        keyword = original keyword used to get node
def get_insights(node: object, keyword: object) -> object:
    insights = []
    conceptnet_url = 'http://api.conceptnet.io'+node+'?format=json'
    data = requests.get(conceptnet_url).json()
    dict_keys = data.keys()
    #print(dict_keys)
    data_len = len(data['edges'])
    #print(data_len)
    edge_counter = 1
    stop_check = 0

    while stop_check is 0:
        if 'view' in dict_keys:   # move on to next page
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
            edge = data['edges'][edge_counter]
            #print(edge['end'].keys())
            label = edge['start']['label']
            if '-' in label:
                label = label.replace('-', ' ')
            elif '_' in label:
                label = label.replace('_', ' ')
            if 'language' in edge['start']:
                language = edge['start']['language']
                if language != 'en':  # check to make sure language is english
                    #print('LANGUAGE ERROR: ', language)
                    edge_counter += 1
                    continue
                else:
                # jaccard distance
                    lowercase_interest = keyword.lower()
                    if ' ' in lowercase_interest:
                        split_interest = lowercase_interest.split(' ')
                        jaccard_set2 = set(split_interest)
                    else:
                        jaccard_set2 = set(lowercase_interest)
                    if ' ' in label:
                        split_item = label.split(' ')
                        jaccard_set1 = set(split_item)
                    else:
                        jaccard_set1 = set(label)

                    #print(jaccard_set1, jaccard_set2)

                    jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)

                    # if insight is too similar, move on to the next insight
                    if jd < 0.3 or lowercase_interest.find(label) > -1:
                        edge_counter += 1
                        continue

            # word stemming
                    ps = PorterStemmer()
                    insight_word_stem = word_tokenize(label)
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
                    elif label in insights:
                        edge_counter += 1
                        continue

                    insights.append(label)
                    print(label)
                    edge_counter += 1
            else:
                edge_counter += 1
                continue
    # after insights are filtered, return final insights list
    return insights[:25]   # change this line to determine how many insights to return

# uses a different api to get more related terms
# INPUT: node = matched node from get_node() function
#        insights = list of related terms from get_insights function
def get_more_related_terms(node, insights):
    # related terms api
    obj = requests.get('http://api.conceptnet.io/related/' + node).json()
    edge_counter = 0
    pg_len = len(obj['related'])

    while edge_counter < pg_len:  # uses jaccard distance and nltk stemming to filter insights
        # print(obj['related'][edge_counter])
        # weight = obj['related'][edge_counter]['weight']
        term = obj['related'][edge_counter]['@id']
        split_term = term.split('/')
        if 'en' not in split_term:
            edge_counter += 1
            continue

        # jaccard distance
        split_node = node.split('/')
        lowercase_interest = split_node[-1].lower()
        if ' ' in lowercase_interest:
            split_interest = lowercase_interest.split(' ')
            jaccard_set2 = set(split_interest)
        else:
            jaccard_set2 = set(lowercase_interest)
        if ' ' in split_term[-1]:
            split_item = split_term[-1].split(' ')
            jaccard_set1 = set(split_item)
        else:
            jaccard_set1 = set(split_term[-1])

        #print(jaccard_set1, jaccard_set2)
        jd = nltk.jaccard_distance(jaccard_set1, jaccard_set2)
        # print('JD #: ', jd)

        # if insight is too similar, move on to the next insight
        if jd < 0.3 or lowercase_interest.find(split_term[-1]) > -1:
            edge_counter += 1
            continue

        # word stemming
        ps = PorterStemmer()
        insight_word_stem = word_tokenize(split_term[-1])
        query_word_stem = word_tokenize(lowercase_interest)
        # print(insight_word_stem, query_word_stem)
        stop_loop = 0
        for word in query_word_stem:
            if stop_loop == 0:
                query_root = ps.stem(word)
                for term in insight_word_stem:
                    insight_root = ps.stem(term)
                    if query_root == insight_root:
                        stop_loop = 1
                        break
        if stop_loop == 1:
            edge_counter += 1
            continue
        elif '_' in split_term[-1]:
            split_term[-1] = split_term[-1].replace('_', ' ')

        insights.append(split_term[-1])
        edge_counter += 1
    return insights[:15]

# main function just to run thru all the functions in the correct order
# INPUT: data = a keyword group (see top of page)
def main_function(data):
    counter = 0
    data_len = len(data)
    while counter < data_len:
        keyword = data[counter]
        node = get_node(keyword)
        print('NODE:', node, '\n')
        if node is None:
            counter += 1
            print('\n')
            continue
        insights = get_insights(node, keyword)
        insights = get_more_related_terms(node, insights)
        related_urls = get_related_urls(node)

        print('KEYWORD:', keyword)
        print(insights)
        print(related_urls)
        counter += 1
        print('\n')
        time.sleep(3)

    #return insights, related_urls

###########################################
# Keyword   Node    Insights    URLs

data = perfect_tags_list
main_function(data)


'''
df = pd.read_csv('Step2_conceptnet_insights_for_PerfectTags - Sheet1.tsv', sep='\t')

for index, row in list(df.iterrows()):
    keyword = row['Keyword']
    node = get_node(keyword)
    if node is None:
        print("Node does not exist\n")
        df.iloc[index, [1]] = 'Node does not exist'
        df.to_csv('list_of_related_terms_conceptnet_output.tsv', sep='\t')
        continue
    insights = get_insights(node, keyword)
    insights = get_more_related_terms(node, insights)
    related_urls = get_related_urls(node)

    row['Keyword'] = keyword
    row['Node'] = node
    row['Insights'] = insights
    row['URLs'] = related_urls
    print(row, '\n')
    df.iloc[index] = row

df.to_csv('conceptnet_insights_for_PerfTags.tsv', sep='\t')
print(df[:15])
'''

'''
# pandas loop
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
    data = get_more_related_terms(node, data)
    related_urls_for_data = get_related_urls(node)

    row['CONCEPT_NET NODE'] = node
    row['INSIGHTS'] = data
    row['RELATED URLS'] = related_urls_for_data
    print(row, '\n')
    df.iloc[index] = row

df.to_csv('list_of_related_terms_conceptnet_output.tsv', sep='\t')
print(df[:15])

'''
