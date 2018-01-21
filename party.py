def user_choose_pokemon_to_switch_to(party):

    pokemon_names = [pokemon.name for pokemon in party]

    while True:
        print('Please choose a Pokemon to switch out to')
        for pokemon_name in pokemon_names:
            print(pokemon_name)
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

def enemy_choose_pokemon_to_switch_to(party):

    # Just send out the first Pokemon in party with non-zero HP

    for index, pokemon in enumerate(party):
        if pokemon.stats['HP'][0] > 0:
            chosen_pokemon_party_index = index

    return chosen_pokemon_party_index

def switch_pokemon(party, index_a, index_b):

    party[index_a], party[index_b] = party[index_b], party[index_a]
