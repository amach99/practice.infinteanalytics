import requests
import json

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

movies = ['Inception'
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
#


# need to match keyword to a node first using containing api, then search for similar terms using the similar api
data = sports
print(len(data))



def get_tags(data):
    index = 0
    # containing insights
    while index < len(data):
        if ' ' in data[index]:
            query = data[index].replace(' ', '+')
        else:
            query = data[index]

        print('INDEX #', index)
        print('QUERY: ', query)

        # get insights
        pin_url = 'http://34.74.185.156:12001/pinterest/insights/containing?query='+query+'&k=500'
        insights = requests.get(pin_url).json()
        print('INSIGHTS: ', insights, '\n')

        index += 1
    return insights

def match_keyTo_tag(insights):
    # get most identical tag
    tag_list = list(insights['data']['insights'])
    insight_index = 0
    print(len(tag_list),'\n')
    while insight_index < len(tag_list):
        if '+' in query:
            query = query.replace('+', ' ')
            print('QUERY:', query)
            print('INDEX:', tag_list[insight_index])
        if query in tag_list[insight_index]:
            keyword = query
            print('KEYWORD: ', keyword)


        insight_index += 1

    return tags

# todo finish match key to tag fucntion


def get_similar_terms():
    index = 0
    diversity = -100
    # similar insights
    while index < len(data) and diversity < 101:
        if ' ' in data[index]:
            keyword = data[index].replace(' ', '+')
        else:
            keyword = data[index]

        print('INDEX #', index)
        print('KEYWORD: ', keyword)

        # get insights
        pin_url = 'http://34.74.185.156:12001/pinterest/insights/similar?tags=' + keyword + '&d=' + str(diversity)
        insights = requests.get(pin_url).json()
        print('INSIGHTS: ', insights, '\n')

        index += 1
        if index == len(data):  # went thru all the indices, need to change diversity and rerun the loop
            index = 0
            diversity += 100
            print('###################################')
            print('DIVERSITY = ', diversity)

        # update values

    return insights
