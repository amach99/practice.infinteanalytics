import requests
import inflect
p = inflect.engine()
import pandas as pd
from nltk.corpus import wordnet

# Keyword clusters
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
                  'Iron Man (character)',
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


# imported pandas to create a df to display results for each keyword
# pandas headers: [QUERY] [Q_GROUP] [TAG] [TAGID] [INSIGHTS]
def main():
    df = pd.read_csv('facebook_insights_for_PerfTags - Sheet1.tsv', sep='\t')  # change input file

    for index, row in list(df.iterrows()):
        query = row['QUERY']
        query_group, tags, insights = FB_insights(query)  # getting data

        # writing to pandas df
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

    df.to_csv('FB_insights_for_PerfTags.tsv', sep='\t')  # change to whatever to create pandas df
    print(df[:15])

    return 0


# given a keyword (query) this function searches thru the keyword clusters and returns the name of the correct group
# that the keyword belongs too and a list of synonyms for the name of the keyword group
def get_query_group(query):
    query_groupID = [('food', id(food)),
                     ('sports', id(sports)),
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
                            syn_list = get_syn(index[0])
                            print(index[0], syn_list)
                            print('Q_GROUP:', index[0])
                            return index[0], syn_list

    print('ERROR: NO MATCHING QUERY GROUP FOR,' + query + '\n')
    return 1


# imported the wordnet to get synonyms for query groups, an attempt to increase the # of related terms for keywords
# used in get_query_group function
# INPUT: word = query group name
def get_syn(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            name = l.name()
            if '_' in l.name():
                name = l.name().replace('_', ' ')
            if name in synonyms:  # if duplicate synonym, skip it
                continue
            else:
                synonyms.append(name)

    return synonyms[:10]


# uses 'http://34.74.185.156:12002/facebook/insights/containing?query=kaffary&k=500' to find a tag that contains
# a specific keyword we want
# INPUT: query = keyword that we want to get related terms for
#        query_group = cluster that keyword is located in  (see above for keyword clusters)
def getFB_nodeID(query, query_group):
    counter = 0
    potentialFBtags_IDlist = []
    fb_url = 'http://34.74.185.156:12002/facebook/insights/containing?query=' + query + '&k=500'
    response = requests.get(fb_url).json()
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
    length = len(response['data']['recommendations'])
    if length == 0:
        print('ERROR: NO POTENTIAL TAGS!')
        return 1  # early exit if no tags containing the keyword are found
    recommendations = response['data']['recommendations']
    print('RECOMMENDATIONS', recommendations, '\n')
    # recommendations are all available tags containing the keyword, can that can be used to get more related terms

    # this loop finds potential matches and adds the to the potentialFBtags_IDlist
    while counter < length:
        nodeID = recommendations[counter][-1]
        node_text = recommendations[counter][1]
        node_group = recommendations[counter][2]
        if '/' in node_group:
            node_group = node_group.replace('/', ' ')
        node = (node_text, node_group, nodeID)
        print(node, '\n')
        if query.lower() in node_text.lower():
            if query.lower() == node_text.lower():
                pFBtag = (node_text, nodeID)
                print('MATCH FOUND:', node)
                return pFBtag
                # if a tag is found that is exactly the same as the keyword, pFBtag is returned and the function ends
            else:
                # imported the inflect library to compare words and find matches even if words are not identical
                # for example movies and movie would would compared and determined to be different versions of the same word
                lowercase_query_group = query_group.lower()
                lowercase_node_group = node_group.lower()
                result = p.compare(lowercase_query_group, lowercase_node_group)
                if result == 'p:s':  # plural:singular
                    if p.singular_noun(lowercase_query_group) in lowercase_node_group:
                        pFBtag = (node_text, nodeID)
                        # print('TAG: ', node_text, '\n')
                        potentialFBtags_IDlist.append(pFBtag)
                elif result == 's:p':  # singular:plural
                    if p.plural(lowercase_query_group) in lowercase_node_group:
                        pFBtag = (node_text, nodeID)
                        # print('TAG: ', node_text, '\n')
                        potentialFBtags_IDlist.append(pFBtag)
                elif result is False or result == 'eq':  # if different words check if keyword exists in node text
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
    # if no perfect tag is found, a list of potential tags is returned


# this function uses 'http://34.74.185.156:12002/facebook/insights/similar?page_id=6530823&b=0' to get similar terms
# INPUT: nodes = potentialFBtags_IDlist or pFBtag (perfect match)
#        query_group = cluster that keyword is located in (see above for keyword clusters)
#        syn_list = list of synonyms for query_group word
def getFB_insights(nodes, query_group, syn_list):
    counter = 0
    related_terms = []
    if nodes == 1:
        return 1  # if potentialFBtagsID_list is empty return 1 for no possible insights

    if type(nodes) is list:  # if multiple potential tags run thru the list and get insights for each one
        while counter < len(nodes):
            nodeID = nodes[counter][-1]
            url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=50'
            response = requests.get(url).json()
            if response:
                print('Success!')
            else:
                print('An error has occurred.')
            recommendations = response['data']['recommendations']
            # all potential related tags for a matched containing tag
            more_related_terms = word_comparison_check(recommendations, query_group)
            if len(more_related_terms) > 0 and more_related_terms != 1:
                related_terms.extend(more_related_terms)
                # compares related tag group with query_group word

                # compares potentially related tag group with synonyms of query_group in an attempt
                # to get more meaningful matches
            for term in syn_list:
                more_related_terms = word_comparison_check(recommendations, term)
                if len(more_related_terms) > 1:
                    related_terms.extend(more_related_terms)
            counter += 1

    elif type(nodes[-1]) is str:  # if only one potential tag, or a perfect tag is returned to us, get insights
        nodeID = nodes[-1]
        url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=50'
        response = requests.get(url).json()
        if response:
            print('Success!')
        else:
            print('An error has occurred.')
        recommendations = response['data']['recommendations']  # all potential related tags for a matched containing tag
        related_terms = word_comparison_check(recommendations, query_group)
        # compares related tag group with query_group word

        # compares potentially related tag group with synonyms of query_group in an attempt
        # to get more meaningful matches
        for term in syn_list:
            more_related_terms = word_comparison_check(recommendations, term)
            if len(more_related_terms) > 1:
                related_terms.extend(more_related_terms)

    elif type(nodes[-1]) is int:  # may or not be necessary, wrote this statement just in case to cover potential bugs
        nodeID = nodes[-1]
        url = 'http://34.74.185.156:12002/facebook/insights/similar?page_id=' + str(nodeID) + '&b=0'
        response = requests.get(url).json()
        if response:
            print('Success!')
        else:
            print('An error has occurred.')
        recommendations = response['data']['recommendations']
        related_terms = word_comparison_check(recommendations, query_group)
        # compares related tag group with query_group word

        # compares potentially related tag group with synonyms of query_group in an attempt
        # to get more meaningful matches
        for term in syn_list:
            more_related_terms = word_comparison_check(recommendations, term)
            if len(more_related_terms) > 1:
                related_terms.extend(more_related_terms)

    try:  # gets rid of duplicate terms in the final related terms list by making it a set
        related_terms = set(related_terms)
    except TypeError:
        print(related_terms)
        return 3000  # random number so I know what went wrong

    return related_terms


# imported the inflect library to compare words and find matches even if words are not identical
# for example movies and movie would would compared and determined to be different versions of the same word
# used in getFB_insights function
# INPUT: recommendations = potential related terms that need to be filtered
#        query_group = name of keyword group that the query belongs too
def word_comparison_check(recommendations, query_group):
    related_terms = []
    node_counter = 0
    while node_counter < len(recommendations):
        insight_node = recommendations[node_counter]
        insight_node_group = insight_node[2]
        if '/' in insight_node_group:
            insight_node_group = insight_node_group.replace('/', ' ')
        insight_node_text = insight_node[1]
        if insight_node_text.isascii() is False:  # TODO need to implement some kind of decode method here
            # insight_node_text = insight_node_text.encode()
            # d_insight_node_text = decode(insight_node_text)
            print('NON ASCII TEXT:', insight_node_text)
            node_counter += 1  # if non ascii text is found, just skip that tag
            continue
        lowercase_query_group = query_group.lower()
        lowercase_insight_node_group = insight_node_group.lower()
        result = p.compare(lowercase_query_group, lowercase_insight_node_group)

        if result == 'p:s':  # plural:singular
            if p.singular_noun(
                    lowercase_query_group) in lowercase_insight_node_group:  # now comparing singular:singular
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
        elif result == 's:p':  # singular:plural
            if p.plural(lowercase_query_group) in lowercase_insight_node_group:  # now comparing plural:plural
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
        elif result is False or result == 'eq':  # if different words check if keyword exists in node text
            if lowercase_query_group in lowercase_insight_node_group:
                pFBtag = insight_node_text
                print('TAG: ', pFBtag, '\n')
                if pFBtag.isspace():
                    print('INVALID TAG\n')
                    continue
                related_terms.append(pFBtag)
            if p.singular_noun(lowercase_query_group):  # evaluates to True or False
                if p.singular_noun(lowercase_query_group) in lowercase_insight_node_group:
                    pFBtag = insight_node_text
                    related_terms.append(pFBtag)

        print(insight_node)
        node_counter += 1

    return related_terms


# main loop to get related terms for a keyword, runs thru all the functions
# INPUT: query = keyword
def FB_insights(query):
    query_group, syn_list = get_query_group(query)
    insights_id = getFB_nodeID(query, query_group)
    if insights_id == 1:
        insights = 1  # in no potential tags are found, set insights to none as well
        return query_group, insights_id, insights

    if type(insights_id) is list:  # if multiple possible results are found, get insights for each
        print('MULTIPLE IDS:', insights_id)
        insights = getFB_insights(insights_id, query_group, syn_list)
    else:
        print('ID:', insights_id)
        insights = getFB_insights(insights_id, query_group, syn_list)

    print('QUERY:', query)
    print('Q_GROUP:', query_group)
    if insights == 1 or len(insights) < 1:
        insights = 1
        print('ERROR: NO INSIGHTS FOUND\n')
    elif insights == 3000:  # error occurred when making related terms list into a set
        print('TYPE ERROR!')
        insights = 1
    else:
        print('INSIGHTS:', insights)

    return query_group, insights_id, insights


# if __name__ == '__main__':
#     main()
