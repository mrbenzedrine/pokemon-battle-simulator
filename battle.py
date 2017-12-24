from type_chart import typeChart


def choose_action(pokemon_name):

    # Choose between the options 'Fight', 'Bag', 'Pokemon' and 'Run'

    available_actions = [
        'Fight',
        'Bag',
        'Pokemon',
        'Run'
    ]
    chosen_action = None
    valid_action_chosen = False

    while valid_action_chosen is False:
        print('\nWhat will %s do?' % pokemon_name)

        # Print out action choices

        for action in available_actions:
            print(action)
        print('\n')
        choice = input()

        for action in available_actions:
            if action == choice:
                valid_action_chosen = True
                chosen_action = choice
                break
            else:
                valid_action_chosen = False

        if valid_action_chosen is False:
            print('That action doesn\'t exist please choose a'
                  ' valid action')
    return chosen_action


def battle(my_pokemon, their_pokemon):

    print("Current HP is %s" % my_pokemon.current_hp)

    while my_pokemon.current_hp > 0 and their_pokemon.stats['HP'] > 0:

        # First need to choose an action (fight, bag, pokemon, run)

        chosen_action = choose_action(my_pokemon.name)

        if chosen_action == 'Fight' or \
            chosen_action == 'Bag' or \
            chosen_action == 'Pokemon' or \
                chosen_action == 'Run':

            # Have all of them call the fight function for now, no idea
            # how to do the bag function and stuff yet =P

            fight(my_pokemon, their_pokemon)

    if my_pokemon.current_hp <= 0:
        print('Your %s has fainted!' % my_pokemon.name)
        # Probably shouldn't be calling update_state_file directly, but
        # just do it for now =P
        my_pokemon.update_state_file()
    if their_pokemon.stats['HP'] <= 0:
        print('Their %s has fainted!' % their_pokemon.name)

        # should then gain some xp for beating the opponent

        my_pokemon.update_xp(50)

    # print('Broken out of battle\'s while loop')
    print('Your %s\'s HP is %s' % (my_pokemon.name, my_pokemon.current_hp))
    print('Their %s\'s HP is %s' % (their_pokemon.name, their_pokemon.stats['HP']))


def fight(my_pokemon, their_pokemon):

    # 'Fight' action

    my_chosen_move = choose_move(my_pokemon, my_pokemon.moves)
    # Make the opponent's Squirtle use Tackle as default for now
    their_chosen_move = their_pokemon.moves['Tackle']

    # Check Speed stats to see who moves first
    # (Won't be Speed stat alone that determines this,
    # but for now it'll do)

    opponent_moves_first = who_moves_first(my_pokemon, their_pokemon)

    # Time for battle now!

    perform_one_round(opponent_moves_first, my_pokemon, my_chosen_move,
                      their_pokemon, their_chosen_move)


def choose_move(my_pokemon, moves):

    # So this is a preliminary section, we're deciding
    # what move to make, so it needs to keep looping back
    # to the start of the move-choosing process if an invalid
    # move is chose, how to do that?

    chosen_move = None
    valid_move_chosen = False
    while valid_move_chosen is False:
        print('\nWhat move do you choose?')

        # Print out move choices

        for move in moves:
            print(move)
        print('\n')
        choice = input()

        for move in moves:
            if choice == move:
                valid_move_chosen = True
                chosen_move = my_pokemon.moves[move]
                break
            else:
                valid_move_chosen = False

        if valid_move_chosen is False:
            print('That move doesn\'t exist, please choose a valid move')

    return chosen_move


def who_moves_first(my_pokemon, their_pokemon):

    # Decide who goes first

    opponent_moves_first = None
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

        if their_pokemon.stats['HP'] <= 0:
            return
        else:
            execute_move(their_pokemon, my_pokemon, their_move)

    elif opponent_moves_first is True:
        # They get to move first, so reverse the order of
        # move execution

        execute_move(their_pokemon, my_pokemon, their_move)

        if my_pokemon.current_hp <= 0:
            return
        else:
            execute_move(my_pokemon, their_pokemon, my_move)


def execute_move(pokemon1, pokemon2, pokemon1_move):

    # pokemon1 is attacking, pokemon2 is defending

    damage_multiplier = move_type_check(pokemon1_move['Type'], pokemon2.type)
    move_damage = pokemon1_move['Power'] * damage_multiplier

    # Set the string for the damage multiplier
    # ie, super effective, not very effective etc

    effectiveness_message = None

    if damage_multiplier == 1:
        pass
    elif damage_multiplier == 1/2:
        # Print not very effective
        effectiveness_message = 'It\'s not very effective...'
    elif damage_multiplier == 2:
        # Print super effective
        effectiveness_message = 'It\'s super effective!'

    # Opponent Pokemon don't need to have a separate value for current HP
    # vs the value of their HP stat, so need to check whether pokemon2.current_hp
    # value exists; if it does, then pokemon2 is a user pokemon so alter current_hp,
    # if it doesn't exist, then it's an opponent pokemon, so just alter its HP stat
    # for now?

    try:
        if pokemon2.current_hp - move_damage / 5 < 0:
            # Just set it to zero, can't have negative HP!
            pokemon2.current_hp = 0
        else:
            pokemon2.current_hp -= move_damage / 5

    except AttributeError:

        if pokemon2.stats['HP'] - move_damage / 5 < 0:
            # Just set it to zero, can't have negative HP!
            pokemon2.stats['HP'] = 0
        else:
            pokemon2.stats['HP'] -= move_damage / 5

    print('%s used %s!' % (pokemon1.name, pokemon1_move['Name']))
    if effectiveness_message is not None:
        print(effectiveness_message)

    try:
        print('%s\'s HP is now %s' % (pokemon2.name, pokemon2.current_hp))
    except AttributeError:
        print('%s\'s HP is now %s' % (pokemon2.name, pokemon2.stats['HP']))

def move_type_check(move_type, opposing_pokemon_type):
    print('The move type is %s, the opposing Pokemon\'s type is %s' %
          (move_type, opposing_pokemon_type))
    damage_multiplier = typeChart[move_type][opposing_pokemon_type]
    print('damage_multipler is: %s' % damage_multiplier)
    return damage_multiplier
