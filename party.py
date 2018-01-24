def switch_out_pokemon(party, player):

    choice_function = {
        'user': user_choose_pokemon_to_switch_to,
        'enemy': get_first_available_pokemon
    }.get(player, None)

    chosen_pokemon_party_index = choice_function(party)
    switch_pokemon(party, 0, chosen_pokemon_party_index)
    print("%s sent out %s!" % (player, party[chosen_pokemon_party_index].name))

def user_choose_pokemon_to_switch_to(party):

    pokemon_names = [pokemon.name for pokemon in party]

    while True:
        print('Please choose a Pokemon to switch out to')
        for pokemon in party:
            print("{}: {}HP".format(pokemon.name, pokemon.stats['HP'][0]))
        print('\n')
        choice = input()

        if choice in pokemon_names:
            chosen_pokemon_party_index = pokemon_names.index(choice)
            chosen_pokemon = party[chosen_pokemon_party_index]
            if chosen_pokemon.stats['HP'][0] > 0:
                break
            else:
                print('%s has 0HP so is unable to fight' % chosen_pokemon.name)
        else:
            print('Invalid Pokemon chosen')

    return chosen_pokemon_party_index

def get_first_available_pokemon(party):

    for index, pokemon in enumerate(party):
        if pokemon.stats['HP'][0] > 0:
            chosen_pokemon_party_index = index

    return chosen_pokemon_party_index

def switch_pokemon(party, index_a, index_b):

    party[index_a], party[index_b] = party[index_b], party[index_a]
