import requests
import time
import pandas as pd

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
        'nestle',
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
              ' Grand Theft Auto: San Andreas',
              'Call of Duty: Black Ops',
              'God of War (series)',
              'Call of Duty: World at War',
              'Minecraft',
              "Assassin's Creed (video game)",
              'God of War (video game)',
              'Grand Theft Auto V',
              'Fortnite'
              ]

nonFiction = [sports, entertainers, food]
fiction = [movies, videoGames, fictional_char]

# containing api
# http://34.74.185.156:12001/pinterest/insights/containing?query=xfinity&k=50
# 'http://34.74.185.156:12001/pinterest/insights/containing?query='+query+'&k=50'
# similar api
# http://34.74.185.156:12001/pinterest/insights/similar?tags='example'&d=[-100,0,100]

# need to match keyword to a node first using containing api, then search for similar terms using the similar api


def get_potential_tags(keyword):
    if ' ' in keyword:
        query = keyword.replace(' ', '+')
    else:
        query = keyword

    print('QUERY: ', query)

    # get insights
    pin_url = 'http://34.74.185.156:12001/pinterest/insights/containing?query=' + query + '&k=500'
    potential_pin_tags = requests.get(pin_url).json()
    print('POTENTIAL TAGS: ', potential_pin_tags, '\n')

    return potential_pin_tags


def match_keyword_toTag(keyword, potential_pin_tags):
    # get most identical tag
    tags_containing_keyword = []
    tag_list = list(potential_pin_tags['data']['insights'])
    print('TAG LIST: ', tag_list, 'TAG_LIST_LEN: ', len(tag_list), '\n')
    insight_index = 0
    while insight_index < len(tag_list):
        tag = tag_list[insight_index]
        print('TAG IS: ', tag)

    # checking if the words are the same by comparing strings
        if keyword.lower() == tag.lower():
            perfect_tag = tag
            print('MATCH FOUND: ', perfect_tag, '\n')
            return perfect_tag
        else:
            tags_containing_keyword.append(tag)

        insight_index += 1

    print('NO EXACT MATCH FOUND\n')
    return tags_containing_keyword[:10]


def get_similar_terms(matched_tag):
    index = 0
    diversity = -100
    insights = []
    sorted_insights = []

    # similar insights
    if type(matched_tag) is str:
        while diversity <= 100:
            print('###################################')
            print('DIVERSITY = ', diversity)

            if ' ' in matched_tag:
                keyword = matched_tag.replace(' ', '+')
            else:
                keyword = matched_tag
            print('KEYWORD: ', keyword)

            # get insights
            pin_url = 'http://34.74.185.156:12001/pinterest/insights/similar?tags=' + keyword + '&d=' + str(diversity)
            response = requests.get(pin_url).json()
            print('INSIGHTS: ', response)
            print('\n')

            if diversity == -100:
                dNeg_100_insights = response['data']['insights']
            if diversity == 0:
                d_0_insights = response['data']['insights']
            if diversity == 100:
                #d_100_insights = response['data']['insights']
                sorted_insights = dNeg_100_insights + d_0_insights
                sorted_insights.sort(key=lambda item: item[1], reverse=True)
                for item in sorted_insights:
                    insights.append(item[0])

            diversity += 100
    else:
        while index < len(matched_tag):
            while diversity <= 100:
                print('###################################')
                print('DIVERSITY = ', diversity)

                if ' ' in matched_tag[index]:
                    keyword = matched_tag[index].replace(' ', '+')
                else:
                    keyword = matched_tag[index]
                print('INDEX #', index)
                print('KEYWORD: ', keyword)

                # get insights
                pin_url = 'http://34.74.185.156:12001/pinterest/insights/similar?tags='+keyword+'&d=' + str(diversity)
                response = requests.get(pin_url).json()
                print('INSIGHTS: ', response)
                print('\n')

                if diversity == -100:
                    dNeg_100_insights = response['data']['insights']
                if diversity == 0:
                    d_0_insights = response['data']['insights']
                if diversity == 100:
                    #d_100_insights = response['data']['insights']
                    new_insights = dNeg_100_insights + d_0_insights
                    sorted_insights.extend(new_insights)
                    diversity = -100
                    break

                diversity += 100

            index += 1

    # update values

    sorted_insights.sort(key=lambda item: item[1], reverse=True)
    for item in sorted_insights:
        insights.append(item[0])

    return insights


def getRT_from_pint(data):
    counter = 0
    data_len = len(data)
    perfect_tags = []

    while counter < data_len:
        ppTags = get_potential_tags(data[counter])
        if len(ppTags['data']['insights']) == 0:
            print('NO POTENTIAL TAGS FOUND!\n')
            counter += 1
            continue

        matched_tags = match_keyword_toTag(data[counter], ppTags)
        print('##########TAGS###########')
        print(matched_tags, '\n')
        #df['Tags'] = matched_tags  # writing to file
        if type(matched_tags) is str:
            perfect_tags.append(matched_tags)


        insights = get_similar_terms(matched_tags)
        print('DATA:', data[counter])
        print('TOTAL INSIGHTS:', insights, '\n')
        #df['Insights'] = insights

        #time.sleep(3)
        counter += 1

    print('PERFECT TAGS', perfect_tags)
    #perfect_tags_list.append(perfect_tags)
    # return insights


# main
# Index(['Keyword', 'Tags', 'Insights'], dtype='object')
df = pd.read_csv('Step 2_ Pinterest insights for - Food - Sheet1.tsv', sep='\t')

for index, row in list(df.iterrows()):
    data = row['Keyword']
    pTags = get_potential_tags(data)
    print('POTENTIAL TAGS: ', pTags)
    tags = match_keyword_toTag(data, pTags)
    print('TAGS: ', tags)
    row['Tags'] = tags
    insights = get_similar_terms(tags)
    print('INSIGHTS: ', insights)
    row['Insights'] = insights
    print(row, '\n')
    df.iloc[index] = row

df.to_csv('pin_insights_for_FOOD.tsv', sep='\t')
print(df[:15])



# TODO fix bug with pandas where perfect tags are not identified and written to the tsv file

'''
# loop to run thru all perfect tags
counter = 0
perfect_tags_list = [['The matrix', 'Star trek', 'The hunger games', 'Logan', 'Iron man', 'Deadpool', 'Marvel entertainment', 'Ghost rider', 'Fantastic four', 'Iron man 3', 'The karate kid', 'Ghostbusters'], ['Devil may cry', 'Minecraft'], ['Luke skywalker', 'Iron man', 'Hulk', 'Spiderman'], ['Sachin tendulkar', 'Virat kohli', 'Cristiano ronaldo', 'Fifa world cup', 'Cricket world cup'], ['Katie holmes', 'Logan paul', 'Jennifer lawrence', 'Jason momoa', 'Morena baccarin'], ['Potato chip', 'Fried chicken', 'Pepsi', 'Mountain dew', 'Biscuits', 'Pineapple', 'Bottled water', 'Kale', 'Coffeemaker', 'Watermelon', 'Ketchup', 'Cream soda', 'Pomegranate', 'Lemon', 'Coca cola zero', 'Doritos', 'Diet coke']]
keyword_clusters = [fiction, nonFiction]
while counter < len(perfect_tags_list):
    data = perfect_tags_list[counter]
    insights = getRT_from_pint(data)
    counter += 1

print(insights)
'''
'''
# big loop to run thru all the clusters
perfect_tags_list = []
keyword_clusters = [fiction, nonFiction]
fiction_len = len(fiction)
nonFiction_len = len(nonFiction)

cluster_counter = 0
while cluster_counter < len(keyword_clusters):
    data_counter = 0
    while data_counter < len(keyword_clusters[cluster_counter]):
        data = keyword_clusters[cluster_counter][data_counter]
        insights = getRT_from_pint(data)
        data_counter += 1

    cluster_counter += 1
    print('\n')

print(perfect_tags_list)
'''

