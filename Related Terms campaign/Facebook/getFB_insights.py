import requests
import pprint
import time
import inflect
p = inflect.engine()
import pandas as pd
from PyDictionary import PyDictionary
dictionary = PyDictionary()

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
perfect_tags_list = ['The matrix', 'Avengers comics', 'Star trek', 'The hunger games', 'Logan', 'Iron man',
                     'Deadpool', 'Marvel entertainment', 'Ghost rider', 'Fantastic four', 'Thor film',
                     'Iron man 3', 'The karate kid', 'Ghostbusters', 'Overwatch video game', 'God of war series',
                     'Devil may cry', 'Minecraft', 'Wolverine character', 'Luke skywalker', 'Iron man', 'Hulk',
                     'Spiderman', 'Sachin tendulkar', 'Virat kohli', 'Cristiano ronaldo', 'Fifa world cup',
                     'Cricket world cup', 'Katie holmes', 'Logan paul', 'Jennifer lawrence', 'Jason momoa',
                     'Morena baccarin', 'Potato chip', 'Fried chicken', 'Pepsi', 'Mountain dew', 'Biscuits',
                     'Pineapple', 'Bottled water', 'Kale', 'Coffeemaker', 'Watermelon', 'Ketchup', 'Cream soda',
                     'Pomegranate', 'Lemon', 'Coca cola zero', 'Doritos', 'Diet coke']
nonFiction = [sports, entertainers, food]
fiction = [movies, videoGames, fictional_char]
clusters = [fiction, nonFiction]


# fb api
# curl 'http://34.74.185.156:12002/facebook/insights/containing?query=kaffary&k=500'
# curl 'http://34.74.185.156:12002/facebook/insights/similar?page_id=6530823&b=0'


def getFB_nodeID(query, query_group):
    counter = 0
    potentialFBtags_IDlist = []
    fb_url = 'http://34.74.185.156:12002/facebook/insights/containing?query=' + query + '&k=500'
    response = requests.get(fb_url).json()
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
    a = pprint.isreadable(response)
    print(a)
    length = len(response['data']['recommendations'])
    if length == 0:
        print('ERROR: NO POTENTIAL TAGS!')
        return 1
    recoms = response['data']['recommendations']
    print('RECOMMENDATIONS', recoms, '\n')

    while counter < length:
        # print(recoms[counter][1:3])
        nodeID = recoms[counter][-1]
        node_text = recoms[counter][1]
        node_group = recoms[counter][2]
        node = (node_text, node_group, nodeID)
        print(node, '\n')
        if query.lower() in node_text.lower():
            if query.lower() == node_text.lower():
                pFBtag = (node_text, nodeID)
                print('MATCH FOUND:', node)
                return pFBtag
            else:
                lowercase_query_group = query_group.lower()
                lowercase_node_group = node_group.lower()
                result = p.compare(lowercase_query_group, lowercase_node_group)
                if result == 'p:s':  # plural:singular
                    if p.singular_noun(lowercase_query_group) in lowercase_node_group:
                        pFBtag = (node_text, nodeID)
                        # print('TAG: ', node_text, '\n')
                        potentialFBtags_IDlist.append(pFBtag)
                elif result == 's:p':
                    if p.plural(lowercase_query_group) in lowercase_node_group:
                        pFBtag = (node_text, nodeID)
                        # print('TAG: ', node_text, '\n')
                        potentialFBtags_IDlist.append(pFBtag)
                elif result is False or result == 'eq':
                    if lowercase_query_group in lowercase_node_group:
                        pFBtag = (node_text, nodeID)
                        # print('TAG: ', node_text, '\n')
                        potentialFBtags_IDlist.append(pFBtag)
                    if p.singular_noun(lowercase_query_group):  # evaluates to True or False
                        if p.singular_noun(lowercase_query_group) in lowercase_node_group:
                            pFBtag = (node_text, nodeID)
                            # print('TAG: ', node_text, '\n')
                            potentialFBtags_IDlist.append(pFBtag)
        counter += 1

    print(query)
    print(potentialFBtags_IDlist)
    if len(potentialFBtags_IDlist) == 0:
        return 1
    print('\n')
    print('#########################################################################')
    return potentialFBtags_IDlist


def getFB_insights(nodes, query_group):
    counter = 0
    related_terms = []
    if nodes == 1:
        return 1

    if type(nodes) is list:
        while counter < len(nodes):
            nodeID = nodes[counter][-1]
            url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=0'
            response = requests.get(url).json()
            if response:
                print('Success!')
            else:
                print('An error has occurred.')
            a = pprint.isreadable(response)
            print(a)
            recommendations = response['data']['recommendations']
            more_related_terms = word_comparison_check(recommendations, query_group)
            if more_related_terms == 1:
                return 1
            related_terms.append(more_related_terms)
            counter += 1

    elif type(nodes[-1]) is str:
        nodeID = nodes[-1]
        url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=0'
        response = requests.get(url).json()
        if response:
            print('Success!')
        else:
            print('An error has occurred.')
        a = pprint.isreadable(response)
        print(a)
        recommendations = response['data']['recommendations']
        related_terms = word_comparison_check(recommendations, query_group)

    elif type(nodes[-1]) is int:
        nodeID = nodes[-1]
        url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=0'
        response = requests.get(url).json()
        if response:
            print('Success!')
        else:
            print('An error has occurred.')
        a = pprint.isreadable(response)
        print(a)
        recommendations = response['data']['recommendations']
        related_terms = word_comparison_check(recommendations, query_group)

    return related_terms


def get_query_group(query):
    query_groupID = [('food', id(food)),
                     ('sports',  id(sports)),
                     ('movies', id(movies)),
                     ('entertainers', id(entertainers)),
                     ('video games', id(videoGames)),
                     ('fictional characters', id(fictional_char))]

    for element in clusters:
        for item in element:
            itemID = id(item)
            for value in item:
                if '(' in value:
                    value = value.replace('(', '')
                if ')' in value:
                    value = value.replace(')', '')
                if query.lower() == value.lower():
                    print(itemID, ':', value)
                    for index in query_groupID:
                        if itemID == index[1]:
                            print('Q_GROUP:', index[0])
                            return index[0]
    print('ERROR: NO MATCHING QUERY GROUP FOR,'+query+'\n')
    return 1


def word_comparison_check(recommendations, query_group):
    related_terms = []
    node_counter = 0
    while node_counter < len(recommendations):
        insight_node = recommendations[node_counter]
        insight_node_group = insight_node[2]
        insight_node_text = insight_node[1]
        lowercase_query_group = query_group.lower()
        lowercase_insight_node_group = insight_node_group.lower()
        result = p.compare(lowercase_query_group, lowercase_insight_node_group)
        if result == 'p:s':  # plural:singular
            if p.singular_noun(lowercase_query_group) in lowercase_insight_node_group:
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
        elif result == 's:p':  # singular:plural
            if p.plural(lowercase_query_group) in lowercase_insight_node_group:
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
        elif result is False or result == 'eq':
            if lowercase_query_group in lowercase_insight_node_group:
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
        print(insight_node)
        node_counter += 1

    if len(related_terms) == 0:
        return 1
    else:
        return related_terms


def FB_insights(query):
    query_group = get_query_group(query)
    insights_id = getFB_nodeID(query, query_group)
    if insights_id == 1:
        insights = []
        return query_group, insights_id, insights
    if type(insights_id) is list:
        print('MULTIPLE IDS:', insights_id)
        insights = getFB_insights(insights_id, query_group)
    else:
        print('ID:', insights_id)
        insights = getFB_insights(insights_id, query_group)

    print('QUERY:', query)
    print('Q_GROUP:', query_group)
    if insights == 1:
        print('ERROR: NO INSIGHTS FOUND\n')
    else:
        print('INSIGHTS:', insights)

    return query_group, insights_id, insights


def main():
    df = pd.read_csv('facebook_insights_for_PerfTags_input.tsv', sep='\t')

    for index, row in list(df.iterrows()):
        query = row['QUERY']
        query_group, tags, insights = FB_insights(query)

        if query_group == 1:
            row['Q_GROUP'] = 'ERROR: NO MATCHING QUERY GROUP'
        else:
            row['Q_GROUP'] = query_group
        if tags == 1:
            row['TAG'] = 'ERROR: NO POTENTIAL TAGS'
        else:
            if type(tags) is list:
                tag_name, tag_id = zip(*tags)
                row['TAG'] = pd.array(tag_name, dtype=object)
                row['TAGID'] = pd.array(tag_id, dtype=object)
            else:
                row['TAG'] = tags[0]
                row['TAGID'] = tags[-1]

        if insights == 1 or len(insights) == 0:
            row['INSIGHTS'] = 'ERROR: NO INSIGHTS'
        elif tags == 1:
            row['INSIGHTS'] = 'ERROR: NO INSIGHTS'
        else:
            row['INSIGHTS'] = insights

        print(row, '\n')
        df.iloc[index] = row

    df.to_csv('FB_insights_for_PerfTags.tsv', sep='\t')
    print(df[:15])

    return 0

# todo work on sorting insights
# TODO add tag name category to pandas df

# def getFB_insights(nodeID, query_group):
#     counter = 0
#     related_terms = []
#     if type(nodeID) is str:
#         url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id='+str(nodeID)+'&b=0'
#         response = requests.get(url).json()
#         if response:
#             print('Success!')
#         else:
#             print('An error has occurred.')
#         a = pprint.isreadable(response)
#         print(a)
#         recommendations = response['data']['recommendations']
#         related_terms = word_comparison_check(recommendations, query_group)
#     elif type(nodeID) is int:
#         url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=0'
#         response = requests.get(url).json()
#         if response:
#             print('Success!')
#         else:
#             print('An error has occurred.')
#         a = pprint.isreadable(response)
#         print(a)
#         recommendations = response['data']['recommendations']
#         related_terms = word_comparison_check(recommendations, query_group)
#     else:
#         while counter < len(nodeID):
#             node = nodeID[counter]
#             url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id='+str(node)+'&b=0'
#             response = requests.get(url).json()
#             if response:
#                 print('Success!')
#             else:
#                 print('An error has occurred.')
#             a = pprint.isreadable(response)
#             print(a)
#             recommendations = response['data']['recommendations']
#             more_related_terms = word_comparison_check(recommendations, query_group)
#             related_terms.append(more_related_terms)
#             counter += 1
#
#     return related_terms


if __name__ == '__main__':
    main()
