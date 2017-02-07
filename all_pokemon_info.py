allPokemon = {
    'Bulbasaur': {
        'type': 'Grass',
        'stats': {
            'HP': 30,
            'Attack': 15,
            'SpecialAttack': 12,
            'Defense': 10,
            'SpecialDefense': 10,
            'Speed': 10
        },
        'moves': {
            'Tackle': {
                'Name': 'Tackle',
                'Type': 'Grass',
                'Category': 'Physical',
                'Power': 50,
                'Accuracy': 1,
                'PP': 35
            },
            'Growl': {
                'Name': 'Growl',
                'Type': 'Normal',
                'Category': 'Status',
                'Power': None,
                'Accuracy': 1,
                'PP': 40
            }
        }
    },
    'Charmander': {
        'type': 'Fire',
        'stats': {
            'HP': 30,
            'Attack': 15,
            'SpecialAttack': 13,
            'Defense': 10,
            'SpecialDefense': 10,
            'Speed': 10
        },
        'moves': {
            'Scratch': {
                'Name': 'Scratch',
                'Type': 'Normal',
                'Category': 'Physical',
                'Power': 40,
                'Accuracy': 1,
                'PP': 35
            },
            'Growl': {
                'Name': 'Growl',
                'Type': 'Normal',
                'Category': 'Status',
                'Power': None,
                'Accuracy': 1,
                'PP': 40
            }
        }
    },
    'Squirtle': {
        'type': 'Water',
        'stats': {
            'HP': 30,
            'Attack': 10,
            'SpecialAttack': 13,
            'Defense': 15,
            'SpecialDefense': 12,
            'Speed': 17
        },
        'moves': {
            'Tackle': {
                'Name': 'Tackle',
                'Type': 'Normal',
                'Category': 'Physical',
                'Power': 0,  # Made zero for the sake of testing exp gain of user pokemon
                'Accuracy': 1,
                'PP': 35
            },
            'Tail Whip': {
                'Name': 'Tail Whip',
                'Type': 'Normal',
                'Category': 'Status',
                'Power': None,
                'Accuracy': 1,
                'PP': 30
            }
        }
    }
}
