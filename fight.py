from type_chart import typeChart

def fight(my_pokemon, their_pokemon):

    my_chosen_move = choose_move(my_pokemon, my_pokemon.moves)
    # Make the opponent's Squirtle use Tackle as default for now
    their_chosen_move = their_pokemon.moves['Tackle']

    # Check Speed stats to see who moves first
    # (Won't be Speed stat alone that determines this,
    # but for now it'll do)

    opponent_moves_first = who_moves_first(my_pokemon, their_pokemon)

    perform_one_round(opponent_moves_first, my_pokemon, my_chosen_move,
                      their_pokemon, their_chosen_move)

def choose_move(my_pokemon, moves):

    while True:
        print('\nWhat move do you choose?')

        for move in moves:
            print(move)
        print('\n')
        choice = input()

        if(choice in moves):
            chosen_move = my_pokemon.moves[choice]
            break
        else:
            print('That move doesn\'t exist, please choose a valid move')

    return chosen_move

def who_moves_first(my_pokemon, their_pokemon):

    if my_pokemon.stats['Speed'] >= their_pokemon.stats['Speed']:
        opponent_moves_first = False
    else:
        opponent_moves_first = True

    return opponent_moves_first

def perform_one_round(opponent_moves_first, my_pokemon, my_move,
                      their_pokemon, their_move):

    if opponent_moves_first is False:
        # We get to move first, time to execute the move

        execute_move(my_pokemon, their_pokemon, my_move)

        if their_pokemon.stats['HP'][0] == 0:
            return
        else:
            execute_move(their_pokemon, my_pokemon, their_move)

    elif opponent_moves_first is True:
        # They get to move first, so reverse the order of
        # move execution

        execute_move(their_pokemon, my_pokemon, their_move)

        if my_pokemon.stats['HP'][0] == 0:
            return
        else:
            execute_move(my_pokemon, their_pokemon, my_move)

def execute_physical_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move):

    move_type_check_result = move_type_check(attacking_pokemon_move['Type'], defending_pokemon)
    damage_multiplier = move_type_check_result[0]
    effectiveness_message = move_type_check_result[1]

    attacking_pokemon.attack(attacking_pokemon_move, damage_multiplier, defending_pokemon)

    print('%s used %s!' % (attacking_pokemon.name, attacking_pokemon_move['Name']))
    if effectiveness_message is not None:
        print(effectiveness_message)

    print('%s\'s HP is now %s' % (defending_pokemon.name, defending_pokemon.stats['HP'][0]))

def move_type_check(attacking_move_type, defending_pokemon):

    print('The attacking move type is %s, the defending Pokemon\'s type is %s' %
          (attacking_move_type, defending_pokemon.type))
    damage_multiplier = typeChart[attacking_move_type][defending_pokemon.type]
    print('damage_multipler is: %s' % damage_multiplier)

    # Check what message, if any, should be returned regarding the effectiveness of the
    # type of the move against the type of the defending pokemon

    effectiveness_message = None

    if damage_multiplier == 0:
        effectiveness_message = 'It doesn\'t affect ' + defending_pokemon.name + '...'
    elif damage_multiplier == 1/2:
        effectiveness_message = 'It\'s not very effective...'
    elif damage_multiplier == 2:
        effectiveness_message = 'It\'s super effective!'

    return (damage_multiplier, effectiveness_message)

def execute_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move):

    # Check if physical attack or status attack move

    if(attacking_pokemon_move['Category'] == 'Physical'):
        execute_physical_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move)
    else:
        execute_status_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move)

def execute_status_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move):

    pass
