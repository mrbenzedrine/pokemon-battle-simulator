from type_chart import typeChart

class Battle():

    def __init__(self, user_pokemon, enemy_pokemon):

        self.user_pokemon = user_pokemon
        self.enemy_pokemon = enemy_pokemon

    def battle(self):

        print("Current HP is %s" % self.user_pokemon.stats['HP'][0])

        while self.user_pokemon.stats['HP'][0] > 0 and self.enemy_pokemon.stats['HP'][0] > 0:

            # First need to choose an action (fight, bag, pokemon, run)

            chosen_action = self.choose_action()

            if chosen_action == 'Fight' or \
                chosen_action == 'Bag' or \
                chosen_action == 'Pokemon' or \
                    chosen_action == 'Run':

                # Have all of them call the fight function for now

                self.fight()

        if self.user_pokemon.stats['HP'][0] == 0:
            print('Your %s has fainted!' % self.user_pokemon.name)
            self.user_pokemon.update_state_file()
        if self.enemy_pokemon.stats['HP'][0] == 0:
            print('Their %s has fainted!' % self.enemy_pokemon.name)

            # should then gain some xp for beating the opponent

            self.user_pokemon.update_xp(50)

        print('Your %s\'s HP is %s' % (self.user_pokemon.name, self.user_pokemon.stats['HP'][0]))
        print('Their %s\'s HP is %s' % (self.enemy_pokemon.name, self.enemy_pokemon.stats['HP'][0]))

        # Reset the stats multipliers of both pokemon

        self.user_pokemon.reset_stat_multipliers()
        self.enemy_pokemon.reset_stat_multipliers()

    def choose_action(self):

        available_actions = [
            'Fight',
            'Bag',
            'Pokemon',
            'Run'
        ]

        while True:
            print('\nWhat will %s do?' % self.user_pokemon.name)

            for action in available_actions:
                print(action)
            print('\n')
            choice = input()

            if choice in available_actions:
                break
            else:
                print('That action doesn\'t exist, please choose a valid action')

        return choice

    def fight(self):

        user_chosen_move = self.choose_move()
        # Make the opponent's Squirtle use Tackle as default for now
        enemy_chosen_move = self.enemy_pokemon.moves['Tackle']

        # Check Speed stats to see who moves first
        # (Won't be Speed stat alone that determines this,
        # but for now it'll do)

        opponent_moves_first = self.who_moves_first()

        self.perform_one_round(opponent_moves_first, user_chosen_move, enemy_chosen_move)

    def choose_move(self):

        while True:
            print('\nWhat move do you choose?')

            for move in self.user_pokemon.moves:
                print(move)
            print('\n')
            choice = input()

            if(choice in self.user_pokemon.moves):
                chosen_move = self.user_pokemon.moves[choice]
                break
            else:
                print('That move doesn\'t exist, please choose a valid move')

        return chosen_move

    def who_moves_first(self):

        if self.user_pokemon.stats['Speed'] >= self.enemy_pokemon.stats['Speed']:
            opponent_moves_first = False
        else:
            opponent_moves_first = True

        return opponent_moves_first

    def perform_one_round(self, opponent_moves_first, user_move, enemy_move):

        if opponent_moves_first:
            first_pokemon = self.enemy_pokemon
            first_pokemon_move = enemy_move
            second_pokemon = self.user_pokemon
            second_pokemon_move = user_move
        else:
            first_pokemon = self.user_pokemon
            first_pokemon_move = user_move
            second_pokemon = self.enemy_pokemon
            second_pokemon_move = enemy_move

        self.execute_move(first_pokemon, second_pokemon, first_pokemon_move)

        if second_pokemon.stats['HP'][0] == 0:
            return
        else:
            self.execute_move(second_pokemon, first_pokemon, second_pokemon_move)


    def execute_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        # Check if physical attack or status attack move

        if(attacking_pokemon_move['Category'] == 'Physical'):
            self.execute_physical_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move)
        else:
            self.execute_status_move(attacking_pokemon, defending_pokemon, attacking_pokemon_move)

    def execute_physical_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        move_type_check_result = self.move_type_check(attacking_pokemon_move['Type'], defending_pokemon)
        damage_multiplier = move_type_check_result[0]
        effectiveness_message = move_type_check_result[1]

        stat_multiplier = attacking_pokemon.stats_multipliers[attacking_pokemon_move['DependentStat']]

        attacking_pokemon.use_physical_move(attacking_pokemon_move, damage_multiplier * stat_multiplier, defending_pokemon)

        print('%s used %s!' % (attacking_pokemon.name, attacking_pokemon_move['Name']))
        if effectiveness_message is not None:
            print(effectiveness_message)

        print('%s\'s HP is now %s' % (defending_pokemon.name, defending_pokemon.stats['HP'][0]))

    def execute_status_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        move_type_check_result = self.move_type_check(attacking_pokemon_move['Type'], defending_pokemon)
        damage_multiplier = move_type_check_result[0]
        effectiveness_message = move_type_check_result[1]

        if attacking_pokemon_move['doesAffectUser']:
            target_pokemon = attacking_pokemon
        else:
            target_pokemon = defending_pokemon

        print('%s used %s!' % (attacking_pokemon.name, attacking_pokemon_move['Name']))
        if damage_multiplier != 0:
            attacking_pokemon.use_status_move(attacking_pokemon_move, attacking_pokemon_move['Power'], target_pokemon)
            affected_stat = attacking_pokemon_move['AffectedStat']
            stat_with_applied_multiplier = round(target_pokemon.stats[affected_stat] * target_pokemon.stats_multipliers[affected_stat])
            print('%s\'s %s stat is now %s' % (target_pokemon.name, affected_stat, stat_with_applied_multiplier))
        else:
            print(effectiveness_message)

    def move_type_check(self, attacking_move_type, defending_pokemon):

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
