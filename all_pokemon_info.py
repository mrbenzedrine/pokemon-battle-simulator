allPokemon = {
    'Bulbasaur': {
        'type': 'Grass',
        'stats': {
            'HP': [30, 30],
            'Attack': 15,
            'SpecialAttack': 12,
            'Defense': 10,
            'SpecialDefense': 10,
            'Speed': 10
        },
        'moves': {
            'Tackle': {
                'Name': 'Tackle',
                'Type': 'Normal',
                'Category': 'Damage',
                'DependentStat' : 'Attack',
                'statusConditionInfliction': 'Possible',
                'alternativeStatusCondition' : 'Paralyzed',
                'Power': 50,
                'Accuracy': 1,
                'PP': 35
            },
            'Growl': {
                'Name': 'Growl',
                'Type': 'Normal',
                'Category': 'Stat',
                'AffectedStat': 'Attack',
                'doesAffectUser': False,
                'Power': -1,
                'Accuracy': 1,
                'PP': 40
            },
            'Poison Powder': {
                'Name': 'Poison Powder',
                'Type': 'Poison',
                'Category': 'StatusCondition',
                'Accuracy': 1,
                'PP': 35
            },
            'Sludge': {
                'Name': 'Sludge',
                'Type': 'Poison',
                'Category': 'Damage',
                'DependentStat': 'SpecialAttack',
                'statusConditionInfliction': 'Possible',
                'Power': 65,
                'Accuracy': 1,
                'PP': 20
            }
        }
    },
    'Charmander': {
        'type': 'Fire',
        'stats': {
            'HP': [30, 30],
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
                'Category': 'Damage',
                'DependentStat' : 'Attack',
                'statusConditionInfliction': 'Nothing',
                'Power': 40,
                'Accuracy': 1,
                'PP': 35
            },
            'Growl': {
                'Name': 'Growl',
                'Type': 'Normal',
                'Category': 'Stat',
                'AffectedStat': 'Attack',
                'doesAffectUser': False,
                'Power': -1,
                'Accuracy': 1,
                'PP': 40
            }
        }
    },
    'Squirtle': {
        'type': 'Water',
        'stats': {
            'HP': [30, 30],
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
                'Category': 'Damage',
                'DependentStat' : 'Attack',
                'statusConditionInfliction': 'Nothing',
                'Power': 30,
                'Accuracy': 1,
                'PP': 35
            },
            'Tail Whip': {
                'Name': 'Tail Whip',
                'Type': 'Normal',
                'Category': 'Stat',
                'AffectedStat': 'Defense',
                'doesAffectUser': False,
                'Power': -1,
                'Accuracy': 1,
                'PP': 30
            }
        }
    }
}
