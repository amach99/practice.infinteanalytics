import getFB_insights
import conceptnet_insights
import pinterest_keyword_insights
import pprint

# keyword_groups
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


def get_final_list(keyword):
    final_insights_list = []

    print('\nFacebook\n')
    fb_q_group, fb_insightsID, fb_insights = getFB_insights.FB_insights(keyword)  # get FB insights

    print('\nPinterest\n')
    pint_insights = pinterest_keyword_insights.getRT_from_pint(keyword)  # get Pinterest insights

    print('\nConceptnet\n')
    cn_insights, cn_related_urls = conceptnet_insights.main_function(keyword)  # get Conceptnet insights

    # if any of the insights return with error code 1, there are no insights for the keyword in that database
    final_insights_list.append('## Facebook ##')
    if fb_insights != 1:
        final_insights_list.append(fb_insights)  # if fb_insights isnt empty add to final_list
    else:
        final_insights_list.append('NO FACEBOOK INSIGHTS')

    final_insights_list.append('## Pinterest ##')
    if pint_insights != 1:
        final_insights_list.append(pint_insights)  # if pint_insights inst empty add to final_list
    else:
        final_insights_list.append('NO PINTEREST INSIGHTS')

    final_insights_list.append('## Conceptnet ##')
    if cn_insights != 1:
        final_insights_list.append(cn_insights)  # if cn_insights isnt empty add to final_list
        final_insights_list.append(cn_related_urls)
    else:
        final_insights_list.append('NO CONCEPTNET INSIGHTS')

    pprint.pprint(final_insights_list)
    return final_insights_list


# a loop that goes thru all the databases and returns one big list
def main():
    data = perfect_tags_list

    if type(data) is not str:  # if data is a list of terms
        for item in data:
            get_final_list(item)
    else:                       # if data is just one term
        get_final_list(data)

    return 0


if __name__ == '__main__':
    main()
